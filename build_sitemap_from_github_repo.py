import streamlit as st
import requests
import uuid
import xml.etree.ElementTree as ET
import boto3
import re
from components.copy import display_copy_button
from components.logger import StreamHandler, display_log, generate_sitemap_dataframe, render_table

logger = StreamHandler.setup_logging()
page_title = 'GitHub Repository Sitemap Generator'

# S3 config
accountid = st.secrets['aws_s3']['accountid'] or ''
access_key_id = st.secrets['aws_s3']['access_key_id'] or ''
access_key_secret = st.secrets['aws_s3']['access_key_secret'] or ''

# S3 buckets setup
@st.cache_resource()
def s3_db():
    s3 = boto3.client('s3',
        endpoint_url = f'https://{accountid}.s3.amazonaws.com/',
        aws_access_key_id = access_key_id,
        aws_secret_access_key = access_key_secret
    )
    return s3

def extract_repo_details(repo_url):
    # Extract owner and repo name
    base_pattern = r"github\.com[:/]([\w-]+)/([\w.-]+)"
    base_match = re.search(base_pattern, repo_url)
    if not base_match:
        raise ValueError("Invalid GitHub repository URL provided.")
    
    owner, repo = base_match.groups()
    
    # Extract branch if present in URL
    branch_pattern = r"/tree/([^/]+(?:/[^/]+)*)"
    branch_match = re.search(branch_pattern, repo_url)
    branch = branch_match.group(1) if branch_match else 'main'
    
    return owner, repo, branch

def get_raw_urls(owner, repo, branch='main'):
    # GitHub API URL to fetch repository contents
    api_url = f'https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1'
    response = requests.get(api_url)
    
    if response.status_code != 200:
        raise ValueError(f"Error accessing repository: {response.json().get('message', 'Unknown error')}")
    
    data = response.json()
    urls = []

    # Base URL for raw content
    base_raw_url = f'https://raw.githubusercontent.com/{owner}/{repo}/{branch}/'

    # Loop through the contents of the repository
    for file in data.get('tree', []):
        if file['type'] == 'blob':
            raw_url = base_raw_url + file['path']
            urls.append(raw_url)

    return urls

def generate_sitemap(urls):
    all_urls = []
    good_urls = 0
    for url in urls:
        st.session_state.logs.append(f"Adding raw URL: {url}")
        logger.info(f"Adding raw URL: {url}")
        all_urls.append(url)
        good_urls += 1
    
    if good_urls > 0:
        st.session_state.logs.append(f"{good_urls} GitHub files were found and added. Generating sitemap ...")
        logger.info(f"{good_urls} GitHub files were found and added. Generating sitemap ...")
        st.success(f"{good_urls} GitHub files were found and added. Generating sitemap ...")
    else:
        st.session_state.logs.append('No files were found in the repository. Sitemap Generation Stopped....')
        logger.error('No files were found in the repository. Sitemap Generation Stopped....')
        st.error("No files were found in the repository.")
        return

    # Create XML Document
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for url in all_urls:
        url_element = ET.SubElement(urlset, "url")
        loc_element = ET.SubElement(url_element, "loc")
        loc_element.text = url

    # Generate the XML sitemap
    sitemap_xml = ET.tostring(urlset, encoding="unicode", method="xml")
    df = generate_sitemap_dataframe(sitemap_xml)

    # Upload to S3
    s3 = s3_db()
    unique_filename = f'{uuid.uuid4()}.xml'
    content_type = 'application/xml'
    s3.put_object(Body=sitemap_xml, Bucket=accountid, Key=unique_filename, ACL='public-read', ContentType=content_type)
    url = f'https://{accountid}.s3.amazonaws.com/{accountid}/{unique_filename}'
    st.session_state.logs.append(f'Successfully generated Sitemap: {url}')
    logger.info(f'Successfully generated Sitemap: {url}')
    st.success("Success! Copy the sitemap link below and use it in CustomGPT.ai to build a RAG-based coding assistant based on your repo files")
    display_copy_button(url)
    render_table(df)

    return sitemap_xml

def main():
    st.sidebar.title('Navigation')
    page = st.sidebar.radio('Go to', ['Home', 'Instructions', 'FAQ'])
    
    if page == 'Home':
        st.info("This free tool lets you build a sitemap from your GitHub repository. This sitemap can then be used to build a RAG-based coding assistant using [CustomGPT.ai](https://customgpt.ai/) that will answer questions and generate code based on your repo's content.")
        
        with st.form(key='github_form'):
            repo_url = st.text_input("Enter your GitHub repository URL:", placeholder="https://github.com/adorosario/github-raw-urls")
            submit_button = st.form_submit_button(label='Generate Sitemap')
            
        if submit_button:
            if repo_url:
                try:
                    owner, repo, branch = extract_repo_details(repo_url)
                    st.session_state.logs.append(f"Found repository: {owner}/{repo} (branch: {branch})")
                    raw_urls = get_raw_urls(owner, repo, branch)
                    generate_sitemap(raw_urls)
                except ValueError as e:
                    st.error(f"Error: {str(e)}")
                    st.session_state.logs.append(f'Error: {str(e)}')
                except Exception as e:
                    st.error(f"An unexpected error occurred: {str(e)}")
                    st.session_state.logs.append(f'Error: {str(e)}')
            else:
                st.error("Please enter a GitHub repository URL")
                st.session_state.logs.append('No repository URL entered')
            display_log(st.session_state.logs)

    elif page == 'Instructions':
        st.header("Instructions")
        st.markdown("""
        1. Enter your GitHub repository URL (eg: https://github.com/adorosario/github-raw-urls)
        2. Click the 'Generate Sitemap' button
        3. Copy the generated sitemap link and use it in [CustomGPT.ai](https://customgpt.ai)
        """)
    
    elif page == 'FAQ':
        st.header("Frequently Asked Questions")
        st.markdown("""
        ### What is this tool?
        This tool creates a sitemap of all raw file URLs in your GitHub repository. This sitemap can be used to create a RAG-based coding assistant that can answer questions and generate code using your repository's content.

        ### What URL formats are supported?
        The tool supports several GitHub repository URL formats:
        - Main branch: `https://github.com/username/repository`
        - Specific branch: `https://github.com/username/repository/tree/branch-name`
        - Repository URLs ending with or without .git
        - Both HTTPS and SSH URLs (e.g., `git@github.com:username/repository.git`)

        ### What types of repositories work best?
        Repositories containing documentation, markdown files, code or other text-based content work best for creating informative chatbots.
        - Large binary files or media files may not be suitable for RAG-based training
        - Documentation and comments in code are valuable. 
        - Markdown (.md) files, especially those containing explanations and documentation, are ideal

        ### Are private repositories supported?
        Currently, this tool only works with public repositories.

        ### How many files can be included?
        The tool supports repositories with up to 50,000 files, which is the standard sitemap limit.

        ### What are the limitations of RAG-based coding assistants?
        While RAG-based assistants can be helpful for code understanding and documentation, they have some important limitations:
        - They cannot execute or test code in real-time
        - They may struggle with complex code dependencies and project structure
        - They work best with well-documented code and may have difficulty with highly abstract or complex implementations
        - They cannot debug code in real-time or provide runtime error analysis
        - Their responses are based on the content in your repository at the time of training, not the current state
        - They may not fully understand the context of code across multiple files or complex dependencies
    
        """)

if __name__ == "__main__":
    st.set_page_config(
        page_title,
        layout='wide',
        initial_sidebar_state='auto',
        menu_items={"About": page_title},
    )
    st.title(page_title)
    st.session_state.logs = []
    main()
