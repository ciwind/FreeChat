from tool.set_context import set_context

# 用户名
user_name = 'User'
gpt_name = 'ChatGPT'
# 头像(svg格式) 来自 https://www.dicebear.com/playground?style=identicon
user_svg = './app/static/ultraman.png'
gpt_svg = './app/static/mind.png'
# 内容背景
user_background_color = 'rgba(225, 230, 235, 0.5)'
gpt_background_color = 'rgba(225, 230, 235, 0.5)'
# 模型初始设置
initial_content_history = [{"role": 'system',
                            "content": '你是一个百事通，回答尽量言简意赅。'}]
initial_content_all = {"history": initial_content_history,
                       "paras": {
                           "temperature": 1.0,
                           "top_p": 1.0,
                           "presence_penalty": 0.0,
                           "frequency_penalty": 0.0,
                       },
                       "contexts": {
                           'context_select': '不设置',
                           'context_input': '',
                           'context_level': 4
                       }}
# 上下文
set_context_all = {"不设置": ""}
set_context_all.update(set_context)

# 自定义css、js
css_code = """
    <style>
    section[data-testid="stSidebar"] > div > div:nth-child(2) {
        padding-top: 0.75rem !important;
    }
    
    section.main > div {
        padding-top: 10px;
    }
    
    section[data-testid="stSidebar"] h1 {
        text-shadow: 2px 2px #ccc;
        font-size: 28px !important;
        font-family: "微软雅黑", "auto";
        margin-bottom: 6px;
        font-weight: 500 !important;
    }
    
    section[data-testid="stSidebar"] .stRadio {
        overflow: overlay;
        height: 28vh;
    }
    
    hr {
        margin-top: 20px;
        margin-bottom: 30px;
    }
    
    .avatar {
        display: flex;
        align-items: center;
        gap: 10px;
        pointer-events: none;
        margin: -8px 10px -16px;
    }
    
    .avatar.user {
        float: right;
    }
    
    .avatar img {
        width: 30px;
        height: 30px;
    }
    
    .avatar h2 {
        font-size: 20px;
        margin: 0;
    }
    
    .content-div {
        padding: 5px 20px;
        margin: 5px;
        text-align: left;
        border-radius: 10px;
        border: none;
        line-height: 1.6;
        font-size: 17px;
    }
    
    .content-div.user p {
        padding: 4px;
        margin: 2px;
        text-align: right;
    }
    
    .content-div.assistant p {
        padding: 4px;
        margin: 2px;
    }
    
    div[data-testid="stForm"] {
        border: none;
        padding: 0;
    }
    
    button[kind="primaryFormSubmit"] {
        border: none;
        padding: 0;
    }
    
    div[data-testid="stForm"] + div[data-testid="stHorizontalBlock"] div[data-baseweb="select"] > div:nth-child(1) {
        background-color: transparent;
        justify-content: center;
        font-weight: 300;
        border-radius: 0.25rem;
        margin: 0;
        line-height: 1.4;
        border: 1px solid rgba(49, 51, 63, 0.2);
    }
    </style>
"""

js_code = """
<script>
function checkElements() {
    const textinput = window.parent.document.querySelector("textarea[aria-label='**输入：**']");   //label需要相对应
    const textarea = window.parent.document.querySelector("div[data-baseweb = 'textarea']");
    const button = window.parent.document.querySelector("button[kind='secondaryFormSubmit']");
    const tabs = window.parent.document.querySelectorAll('button[data-baseweb="tab"] p');
    const tabs_div = window.parent.document.querySelector('div[role="tablist"]');
    const tab_panels = window.parent.document.querySelectorAll('div[data-baseweb="tab-panel"]');

    if (textinput && textarea && button && tabs && tabs_div && tab_panels) {
        // 双击点位输入框，同时抑制双击时选中文本事件
        window.parent.document.addEventListener('dblclick', function (event) {
            let activeTab = tabs_div.querySelector('button[aria-selected="true"]');
            if (activeTab.querySelector('p').textContent === '💬 聊天') {
                textinput.focus();
            } else {
                tabs[0].click();
                const waitMs = 50;

                function waitForFocus() {
                    if (window.parent.document.activeElement === textinput) {
                    } else {
                        setTimeout(function () {
                            textinput.focus();
                            waitForFocus();
                        }, waitMs);
                    }
                }

                waitForFocus();
            }
        });
        window.parent.document.addEventListener('mousedown', (event) => {
            if (event.detail === 2) {
                event.preventDefault();
            }
        });
        textinput.addEventListener('focusin', function (event) {
            event.stopPropagation();
            textarea.style.borderColor = 'rgb(255,75,75)';
        });
        textinput.addEventListener('focusout', function (event) {
            event.stopPropagation();
            textarea.style.borderColor = 'white';
        });

        // Ctrl + Enter快捷方式
        window.parent.document.addEventListener("keydown", event => {
            if (event.ctrlKey && event.key === "Enter") {
                if (textinput.textContent !== '') {
                    button.click();
                }
                textinput.blur();
            }
        });

        // 设置 Tab 键
        textinput.addEventListener('keydown', function (event) {
            if (event.keyCode === 9) {
                // 阻止默认行为
                event.preventDefault();
                if (!window.parent.getSelection().toString()) {
                    // 获取当前光标位置
                    const start = this.selectionStart;
                    const end = this.selectionEnd;
                    // 在光标位置插入制表符
                    this.value = this.value.substring(0, start) + '\t' + this.value.substring(end);
                    // 将光标移动到插入的制表符之后
                    this.selectionStart = this.selectionEnd = start + 1;
                }
            }
        });

        // 处理tabs 在第一次切换时的渲染问题
        tabs.forEach(function (tab, index) {
            const tab_panel_child = tab_panels[index].querySelectorAll("*");

            function set_visibility(state) {
                tab_panels[index].style.visibility = state;
                tab_panel_child.forEach(function (child) {
                    child.style.visibility = state;
                });
            }

            tab.addEventListener("click", function (event) {
                set_visibility('hidden')

                let element = tab_panels[index].querySelector('div[data-testid="stVerticalBlock"]');
                let main_block = window.parent.document.querySelector('section.main div[data-testid="stVerticalBlock"]');
                const waitMs = 50;

                function waitForLayout() {
                    if (element.offsetWidth === main_block.offsetWidth) {
                        set_visibility("visible");
                    } else {
                        setTimeout(waitForLayout, waitMs);
                    }
                }

                waitForLayout();
            });
        });
    } else {
        setTimeout(checkElements, 100);
    }
}

checkElements()
</script>
"""
