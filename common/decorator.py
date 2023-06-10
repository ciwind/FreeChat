import streamlit as st
from common.logger import logger


def handle_exception(func):
    def catch(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(e)
            st.error("程序出现错误，请重试。")
    return catch
