import logging
import streamlit.components.v1 as components
import xml.etree.ElementTree as ET
import pandas as pd

class StreamHandler(logging.Handler):
    def setup_logging():
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger()
        return logger


def render_table(df):
    df_html = df.to_html(index=False, classes="table table-striped table-bordered", border=0, table_id="table")
    display_table(df_html)

def display_log(log_messages):
    components.html(f"""
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
            <button id="toggleButton" class='btn btn-info'>Show log</button>
            <div id="log" style="overflow-y: scroll; display: none; border-radius: 10px; background-color: whitesmoke; padding: 10px; margin-top: 10px; height: 300px;">
            </div>
            <script>

            var logData = {log_messages};
            var logDiv = document.getElementById("log");
            var button = document.getElementById("toggleButton");

            for (var i = 0; i < logData.length; i++) {{
                var para = document.createElement("p");
                var node = document.createTextNode(logData[i]);
                para.appendChild(node);
                logDiv.appendChild(para);
            }}

            button.addEventListener('click', function() {{
                if (logDiv.style.display === "none") {{
                    logDiv.style.display = "block";
                    button.textContent = "Hide log";
                }} else {{
                    logDiv.style.display = "none";
                    button.textContent = "Show log";
                }}
            }});
            </script>
            """, height=500, scrolling=True)

def display_table(df_html):
    components.html(f"""
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
            <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.25/css/dataTables.bootstrap.min.css"/>

            <script type="text/javascript" src="https://code.jquery.com/jquery-3.5.1.js"></script>
            <script type="text/javascript" src="https://cdn.datatables.net/1.10.25/js/jquery.dataTables.min.js"></script>
            <script type="text/javascript" src="https://cdn.datatables.net/1.10.25/js/dataTables.bootstrap.min.js"></script>
            <script type="text/javascript" src="https://cdn.datatables.net/buttons/1.3.1/js/dataTables.buttons.min.js"></script> 
            <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.1.3/jszip.min.js"></script>
            <script type="text/javascript" src="https://cdn.datatables.net/buttons/1.3.1/js/buttons.html5.min.js"></script>
            {df_html if df_html else ''}
            <script>
            $(document).ready(function() {{
                if($('#table').length > 0){{
                    $('#table').DataTable({{
                        "dom": 'Bfrtip',  
                        "pageLength": 10, // Set the number of rows per page
                        "paging": true, // Enable pagination
                        "lengthChange": true, // Disable the ability to change the number of rows per page
                        "searching": true, // Disable search functionality
                        "ordering": true, // Enable column sorting
                        "info": true, // Enable table information display
                        "buttons": [
                            'csvHtml5', 'excelHtml5'
                        ]
                    }});
                }}
            }});
            </script>
            <style>
                .dt-button{{
                    -webkit-text-size-adjust: 100%;
                    -webkit-tap-highlight-color: rgba(0,0,0,0);
                    font-family: "Helvetica Neue",Helvetica,Arial,sans-serif;
                    box-sizing: border-box;
                    text-decoration: none;
                    display: inline-block;
                    padding: 6px 12px;
                    margin-bottom: 0;
                    font-size: 14px;
                    font-weight: 400;
                    line-height: 1.42857143;
                    text-align: center;
                    white-space: nowrap;
                    vertical-align: middle;
                    touch-action: manipulation;
                    cursor: pointer;
                    user-select: none;
                    background-image: none;
                    border: 1px solid transparent;
                    border-radius: 4px;
                    color: #fff;
                    background-color: #337ab7;
                    border-color: #2e6da4;
                }}
            </style>
        """, height=500, scrolling=True)


def generate_sitemap_dataframe(xml):
    root = ET.fromstring(xml)
    data = []
    for url in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
        obj = {}
        loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
        obj['loc'] = loc
        lastmod_element = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod')
        lastmod = lastmod_element.text if lastmod_element is not None else None
        if lastmod:
            obj['lastmod'] = lastmod

        # Append the data to the list
        data.append(obj)

    df = pd.DataFrame(data)
    return df