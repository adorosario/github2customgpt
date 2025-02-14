import streamlit.components.v1 as components

def display_copy_button(download_link):
    components.html(
        f"""
    <style>
        .link-copy-container {{
            margin-top: 27px;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: #f3f3f3;
            padding: 20px;
            border-radius: 10px;
        }}
        .link-input {{
            font-family: monospace;
            width: 80%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            outline: none;
        }}
        .copy-button {{
            display: inline-block;
            background-color: white;
            color: black;
            padding: 10px 15px;
            margin-left: 10px;
            border-radius: 5px;
            cursor: pointer;
        }}
        .copy-button:hover {{
            background-color: ghostwhite;
        }}
        .tooltip {{
          position: relative;
          display: inline-block;
          cursor: pointer;
        }}

        .tooltip .tooltiptext {{
            visibility: hidden;
            width: 120px;
            background-color: white;
            color: black;
            text-align: center;
            border-radius: 6px;
            padding: 5px 0;
            position: absolute;
            z-index: 1;
            bottom: 48px;
            right: -30px;
            border: 1px solid;
        }}

        .tooltip.active .tooltiptext {{
          visibility: visible;
        }}
        .tooltiptext::before {{
            background-color: white;
            content: "";
            display: block;
            height: 16px;
            width: 16px;
            position: absolute;
            bottom: -7.5px;
            z-index: -1;
            left: 52px;
            transform: rotate(47deg) skew(5deg);
            -moz-transform: rotate(47deg) skew(5deg);
            -ms-transform: rotate(47deg) skew(5deg);
            -o-transform: rotate(47deg) skew(5deg);
            -webkit-transform: rotate(47deg) skew(5deg);
            box-shadow: 2px 2px 2px 0 rgba( 178, 178, 178, .4 );
        }}
    </style>
    <div class="link-copy-container">
        <input id="link-input" class="link-input" type="text" value="{download_link}" readonly />
        <div class="tooltip">
            <div class="tooltiptext">
                <span >Copied!</span>
            </div>
            <button id='copy-button' class='copy-button' data-tippy-content="Tooltip">Copy</button>
        </div>
    </div>
    <script>
        function copy(){{
            navigator.clipboard.writeText(document.getElementById('link-input').value);
        }}
        document.addEventListener('DOMContentLoaded', function(){{
            var tooltip = document.querySelector('.tooltip');
            tooltip.addEventListener('focusout', function() {{
              if (this.classList.contains('active')) {{
                this.classList.remove('active');
              }}
            }});

            document.getElementById('copy-button').addEventListener('click', function(){{
                copy();
            }});
            
            tooltip.addEventListener('click', function() {{
              if (this.classList.contains('active')) {{
                this.classList.remove('active');
              }} else {{
                this.classList.add('active');
              }}
            }});
        }})
    </script>
    """,
        height=100)