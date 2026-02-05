
import streamlit as st
import sympy as sp
import re
import numpy as np
from scipy.fft import fft

# ---------------- SYMBOLS ----------------
x, y, z, t, s = sp.symbols('x y z t s')
theta = sp.symbols('theta', real=True)

# ---------------- DEGREE BASED TRIG ----------------
def sin_d(a): return sp.sin(sp.rad(a))
def cos_d(a): return sp.cos(sp.rad(a))
def tan_d(a): return sp.tan(sp.rad(a))

locals_dict = {
    "sin": sin_d,
    "cos": cos_d,
    "tan": tan_d,
    "pi": sp.pi,
    "theta": theta,
    "sqrt": sp.sqrt,
    "log": sp.log,
    "exp": sp.exp
}

# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="Gen-AI Math Solver", layout="centered")

st.title("🧠 Gen-AI Mathematics Solver")
st.subheader("Student-Friendly | Supports `sin 60`, equations, calculus")

st.markdown("""
**Examples you can try:**
- `sin 60`
- `sin^2 30 + cos^2 30`
- `x^2 - 5*x + 6 = 0`
- `d/dx x^2*sin(x)`
- `int x^2`
""")

query = st.text_input("✍️ Enter your math problem:")

if query:
    try:
        q = query.lower()
        q = q.replace("^", "**")

        # Allow "sin 60" style input
        q = re.sub(r'sin\s+(\d+)', r'sin(\1)', q)
        q = re.sub(r'cos\s+(\d+)', r'cos(\1)', q)
        q = re.sub(r'tan\s+(\d+)', r'tan(\1)', q)

        # ---------------- EQUATIONS ----------------
        if "=" in q:
            lhs, rhs = q.split("=")
            lhs = sp.sympify(lhs, locals=locals_dict)
            rhs = sp.sympify(rhs, locals=locals_dict)
            expr = lhs - rhs

            if expr.free_symbols:
                solution = sp.solve(expr)
                st.success("✅ Solution:")
                st.write(solution)
            else:
                result = "TRUE" if sp.simplify(expr) == 0 else "FALSE"
                st.success("✅ Result:")
                st.write(result)

        # ---------------- DERIVATIVE ----------------
        elif q.startswith("d/d"):
            var = q[3]
            expr = sp.sympify(q[4:], locals=locals_dict)
            result = sp.diff(expr, sp.Symbol(var))
            st.success("✅ Derivative:")
            st.write(result)

        # ---------------- INTEGRAL ----------------
        elif q.startswith("int"):
            expr = sp.sympify(q[3:], locals=locals_dict)
            result = sp.integrate(expr)
            st.success("✅ Integral:")
            st.write(result)

        # ---------------- FFT ----------------
        elif q.startswith("fft"):
            signal = eval(q.replace("fft", ""))
            result = fft(signal)
            st.success("✅ FFT Result:")
            st.write(result)

        # ---------------- GENERAL MATH ----------------
        else:
            result = sp.sympify(q, locals=locals_dict)
            st.success("✅ Answer:")
            st.write(sp.simplify(result))

    except Exception as e:
        st.error("❌ Invalid or unsupported math input")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("🔢 Built using SymPy + Streamlit | Degree-based Trigonometry")
