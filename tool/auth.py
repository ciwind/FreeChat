import streamlit as st
import secrets
import string
from tool.chat import ChatGPT
import json


class Cookie:
    key = st.secrets.get('auth', {}).get('cookie_key', '')
    valid_cookies = st.secrets.get('auth', {}).get('valid_cookies', '').split(' ')

    def __init__(self, manager):
        self.manager = manager

    @staticmethod
    def random(length=32):
        characters = string.ascii_letters + string.digits
        random_string = ''.join(secrets.choice(characters) for _ in range(length))
        return 'easyai-' + random_string

    def get(self, cookie_key=''):
        cookie_key = cookie_key or Cookie.key
        return self.manager.get(cookie=cookie_key)

    def is_valid(self, value=None):
        value = value or self.get()
        return '' != value and value is not None and value in Cookie.valid_cookies

    def generate(self):
        value = Cookie.random()
        self.manager.set(Cookie.key, value)

    def get_status(self):
        value = self.get()
        return value, '' != value and value is not None and value in Cookie.valid_cookies

    def set(self, key, value, expire_day=1):
        from datetime import datetime, timedelta
        expires_at = datetime.now() + timedelta(days=expire_day)
        print(f'set {key}={value} expires_at={expires_at}')
        self.manager.set(key, value, expires_at=expires_at)


class Auth:
    st_auth_api_key = 'auth_api_key'
    st_auth_password = 'auth_password'
    st_auth_status = 'auth_status'
    state_valid_password = 'valid_password'
    state_valid_api_key = 'valid_api_key'

    @staticmethod
    def match_password(password):
        return password != '' and password is not None and st.secrets.get('auth', {}).get('password', '') == password

    @staticmethod
    def valid_password(cookie, session_state):
        return Auth.match_password(session_state.get(Auth.state_valid_password, ''))

    @staticmethod
    @st.cache_data
    def valid_api_key(api_key):
        return '' != api_key and api_key is not None and ChatGPT.valid_api_key(api_key)

    @staticmethod
    def get_api_key(cookie, session_state):
        return ChatGPT.api_key \
            if cookie.is_valid() or Auth.valid_password(cookie, session_state) \
            else session_state.get(Auth.state_valid_api_key, '')

    @staticmethod
    def auth_status(cookie, session_state):
        valid = cookie.is_valid() \
                or session_state.get(Auth.state_valid_api_key, '') not in ('', None)\
                or session_state.get(Auth.state_valid_password, '') not in ('', None)
        return valid

    @staticmethod
    def login(cookie, session_state):
        status = Auth.auth_status(cookie, session_state)
        if status:
            st.sidebar.text('认证状态：通过')

        if st.sidebar.checkbox(
                '打开认证' if status else '请先认证',
                value=not status,
                disabled=not status,
                key='auth_switch'):
            st.header('🔐 认证')
            tab_code, tab_password, tab_api_key = st.tabs(['暗号', '密码', 'ApiKey'])
            with tab_code:
                value, valid = cookie.get_status()
                st.code(value)
                st.markdown('状态：%s' % ('有效' if valid else '无效。联系管理员添加。'))
                if st.button(
                        '生成暗号（然后找管理员加权限）' if not value else '重新生成（将失去权限）' if valid else '重新生成',
                        key='generate_cookie'):
                    cookie.generate()

            with tab_password:
                password = st.text_input(
                    '密码', type='password', key=Auth.st_auth_password,
                    value=session_state.get(Auth.state_valid_password, ''),
                    placeholder='访问密码，联系管理员', label_visibility='collapsed')
                if password:
                    if not Auth.match_password(password):
                        st.error('密码无效')
                        cookie.set(Auth.state_valid_password, '')
                    else:
                        st.info('密码认证通过')

            with tab_api_key:
                api_key = st.text_input(
                    'ApiKey', type='password', key=Auth.st_auth_api_key,
                    value=session_state.get(Auth.state_valid_api_key, ''),
                    placeholder='api_key，gpt-3.5-turbo', label_visibility='collapsed')
                if api_key:
                    if not Auth.valid_api_key(api_key):
                        st.error('api_key无效')
                    else:
                        st.info('api_key认证通过')
        return status
