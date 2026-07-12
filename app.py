import streamlit as st

def fibonacci(n):
    """Calculate the nth Fibonacci number."""
    if n < 0:
        return None
    elif n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

st.set_page_config(page_title="Fibonacci Generator", layout="centered")
st.title("Fibonacci Number Generator")
st.write("Enter a number to calculate its Fibonacci value")

n = st.number_input("Enter a number:", min_value=0, step=1, format="%d")

if st.button("Calculate Fibonacci"):
    result = fibonacci(int(n))
    st.success(f"The {int(n)}th Fibonacci number is: {result}")
