import openai
import streamlit as st
from common.logger import logger


class ChatGPT:
    api_key = st.secrets.get("openai", {}).get("api_key", "")

    @staticmethod
    def valid_api_key(api_key):
        try:
            openai.api_key = api_key
            models = openai.Model.list()
        except Exception as e:
            logger.error("API key is invalid. Error:", e)
            return False
        else:
            return True

    @staticmethod
    def chat(api_key, session_state, history_need_input, paras_need_input, current_chat, area_error, stream_mode=False):
        r = ''
        try:
            openai.api_key = api_key
            response = openai.ChatCompletion.create(
                model=st.session_state['select_model'],
                stream=stream_mode,
                messages=history_need_input,
                **paras_need_input)
            if not stream_mode:
                choices = response.get('choices', [])
                if choices:
                    r = choices[0].get('message', {}).get('content', '')
            else:
                r = response
        except openai.error.AuthenticationError:
            area_error.error("无效的 OpenAI API Key。")
        except openai.error.APIConnectionError as e:
            area_error.error("连接超时，请重试。报错：\n" + str(e.args[0]))
        except openai.error.InvalidRequestError as e:
            area_error.error("无效的请求，请重试。报错：\n" + str(e.args[0]))
        except openai.error.RateLimitError as e:
            area_error.error("请求速率过快，请重试。报错：\n" + str(e.args[0]))
        else:
            session_state["chat_of_r"] = current_chat
            session_state["r"] = r
            st.experimental_rerun()
