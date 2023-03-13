import validators

def check_url_is_valid(url: str) -> bool:
    if url is None:
        return False
    if not validators.url(url):
        return False
    return True


# import streamlit as st
# from itertools import cycle

# filteredImages = [] # your images here
# caption = [] # your caption here
# cols = cycle(st.columns(4)) # st.columns here since it is out of beta at the time I'm writing this
# for idx, filteredImage in enumerate(filteredImages):
#     next(cols).image(filteredImage, width=150, caption=caption[idx])