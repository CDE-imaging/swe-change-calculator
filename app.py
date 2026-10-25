import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Liver SWE Change Calculator", page_icon="📋", layout="wide", initial_sidebar_state="collapsed")

# Research prototype: verify coefficients and MDC95 interpretation before publication.
MDC95 = 4.41
EFFECTS = {
    "GE": {"Curvilinear": 0.0, "Linear": 2.14},
    "Siemens": {"Curvilinear": -2.72},
    "SuperSonic": {"Curvilinear": -0.42, "Linear": 0.48},
}

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"], [data-testid="stApp"] {font-family:'DM Sans',sans-serif;}
[data-testid="stAppViewContainer"] {background:#f5f8fc;}
.block-container {max-width:1190px;padding-top:2.2rem;padding-bottom:3.5rem;}
header[data-testid="stHeader"] {background:transparent;}
h1,h2,h3,p {color:#142d51;}
[data-testid="stVerticalBlockBorderWrapper"] > div {border-radius:17px!important;}
[data-testid="stNumberInput"] input,[data-testid="stSelectbox"]>div>div {background:#fff;border-radius:9px;}
[data-testid="stMetric"] {background:#f7faff;border:1px solid #e6edf6;border-radius:14px;padding:18px 20px;min-height:130px;}
[data-testid="stMetricLabel"] {color:#60758e;font-size:0.92rem;}
[data-testid="stMetricValue"] {color:#183763;font-weight:800;font-size:1.85rem;}
[data-testid="stExpander"] {border:1px solid #e4ebf5;background:#fff;border-radius:13px;}
[data-testid="stAlert"] {border-radius:12px;}
.hero {padding:7px 0 21px;display:flex;align-items:center;justify-content:space-between;gap:18px;}
.hero-title {font-size:2.05rem;font-weight:800;letter-spacing:-.035em;color:#102c56;line-height:1.15;}
.hero-sub {color:#6b819d;font-size:1rem;margin-top:7px;}
.pill {background:#e6f0ff;color:#2463b4;border-radius:7px;padding:7px 12px;font-size:.82rem;font-weight:700;display:inline-block;}
.hero-note {font-size:.75rem;color:#8494aa;margin-top:7px;text-align:right;}
.section-heading {font-size:1.16rem;font-weight:800;color:#153563;margin:4px 0 16px;}
.step {display:inline-flex;background:#2c69cb;color:white;border-radius:50%;width:29px;height:29px;align-items:center;justify-content:center;font-size:.85rem;margin-right:9px;}
.panel-title {font-weight:800;color:#194f9a;font-size:1.03rem;margin-bottom:8px;}
.panel-title.green {color:#14765f;}
.small-label {color:#617791;font-size:.85rem;margin:4px 0;}
.result-title {font-size:1.03rem;font-weight:800;color:#163660;margin:6px 0 5px;}
.footnote {font-size:.77rem;color:#8291a5;}
</style>""", unsafe_allow_html=True)

st.markdown("""<div class='hero'><div><div class='hero-title'>Liver SWE Change Calculator</div><div class='hero-sub'>For Post-Kasai portoenterostomy surveillance</div></div><div><div class='pill'>RESEARCH TOOL</div><div class='hero-note'>Not a validated clinical decision tool</div></div></div>""",unsafe_allow_html=True)
st.markdown(
    """
    This calculator was developed based on a study of shear wave
    elastography (SWE) measurement variability in pediatric patients
    after Kasai portoenterostomy (KPE). It estimates longitudinal
    changes in liver stiffness by accounting for systematic
    differences between ultrasound systems and transducers.

    The equipment-adjusted change is compared with the
    study-derived minimal detectable change (MDC95) of
    **4.41 kPa** to assess whether the change exceeds
    estimated measurement variability.
    """
)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("<div class='section-heading'><span class='step'>1</span> Enter examinations</div>", unsafe_allow_html=True)
    left, right = st.columns(2, gap="medium")
    with left:
        with st.container(border=True):
            st.markdown("<div class='panel-title'>▦ Baseline examination</div>",unsafe_allow_html=True)
            a,b=st.columns(2)
            with a:
                b_sys=st.selectbox("Ultrasound system",list(EFFECTS),index=0,key="bs")
            with b:
                b_probe=st.selectbox("Transducer",list(EFFECTS[b_sys]),key="bp")
            b_val=st.number_input("Liver stiffness (kPa)",min_value=0.0,value=8.0,step=.1,format="%.1f",key="bv")
    with right:
        with st.container(border=True):
            st.markdown("<div class='panel-title green'>▦ Follow-up examination</div>",unsafe_allow_html=True)
            a,b=st.columns(2)
            with a:
                f_sys=st.selectbox("Ultrasound system",list(EFFECTS),index=1,key="fs")
            with b:
                f_probe=st.selectbox("Transducer",list(EFFECTS[f_sys]),key="fp")
            f_val=st.number_input("Liver stiffness (kPa)",min_value=0.0,value=6.0,step=.1,format="%.1f",key="fv")

# Calculator
observed=f_val-b_val
bias=EFFECTS[f_sys][f_probe]-EFFECTS[b_sys][b_probe]
adjusted=observed-bias
exceeds=abs(adjusted)>MDC95

with st.container(border=True):
    st.markdown("<div class='section-heading'><span class='step'>2</span> Results</div>",unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    c1.metric("Observed change",f"{observed:+.2f} kPa",help="Follow-up minus baseline")
    c2.metric("Equipment bias",f"{bias:+.2f} kPa",help="Difference in fitted equipment effects")
    c3.metric("Bias-adjusted change",f"{adjusted:+.2f} kPa",help="Observed change minus equipment bias")

    st.markdown(
    """
    <div style="margin:18px 0 0;">
        <div class="result-title">
            ⓘ &nbsp; Adjusted SWE change vs. MDC<sub>95</sub>
        </div>
        <div style="font-size:.88rem;color:#587094;margin-top:4px;">
            MDC<sub>95</sub> = ±4.41 kPa
        </div>
    </div>
    """,
    unsafe_allow_html=True)
    
    # st.markdown("""<div style="display:flex;justify-content:space-between;align-items:center;gap:14px;margin:18px 0 0">
    #   <div class="result-title" style="margin:0">ⓘ &nbsp; Adjusted SWE change vs. MDC<sub>95</sub></div>
    #   <div style="font-size:.91rem;color:#587094">MDC<sub>95</sub> = ±4.41 kPa</div>
    # </div>""",unsafe_allow_html=True)

    # Keep a consistent ±10 kPa scale for ordinary values; expand symmetrically
    # when the result is outside that range.
    import math
    lim=max(10, int(math.ceil((abs(adjusted)+0.8)/2)*2))
    accent="#09865e" if not exceeds else "#df663c"
    fig=go.Figure()
    # Gentle colored zones above the reference axis.
    for lo,hi,fill in [(-lim,-MDC95,"#fff0e8"),(-MDC95,MDC95,"#dcf5e9"),(MDC95,lim,"#fff0e8")]:
        fig.add_shape(type="rect",x0=lo,x1=hi,y0=0.0,y1=0.48,
                      fillcolor=fill,line=dict(width=0),layer="below")
    # Baseline and regularly spaced axis ticks.
    fig.add_shape(type="line",x0=-lim,x1=lim,y0=0,y1=0,
                  line=dict(color="#617996",width=1.5))
    for tick in range(-lim,lim+1,2):
        fig.add_shape(type="line",x0=tick,x1=tick,y0=0,y1=-0.13,
                      line=dict(color="#9badc2",width=1))
        if tick not in (-4, 0, 4):
            fig.add_annotation(x=tick,y=-0.26,text=str(tick).replace("-","−"),
                               showarrow=False,font=dict(size=12,color="#526a8c"))
    fig.add_annotation(x=0,y=-0.26,text="0",showarrow=False,
                       font=dict(size=12,color="#526a8c"))
    # MDC95 threshold lines and labels.
    for bound in (-MDC95,MDC95):
        fig.add_shape(type="line",x0=bound,x1=bound,y0=-0.18,y1=0.59,
                      line=dict(color="#e66d40",width=1.7,dash="dash"))
        fig.add_annotation(x=bound,y=-0.26,text=f"<b>{'−' if bound<0 else ''}4.41</b>",
                           showarrow=False,font=dict(size=12,color="#17375f"),
                           bgcolor="#f5f8fc",borderpad=1)
    # Three balanced headings, matching the reference figure.

    outer = (lim + MDC95) / 2
    for x, label, color in [
        (-outer, "Decreased", "#d85b2f"),
        (0, "Within MDC₉₅", "#00765d"),
        (outer, "Increased", "#d85b2f")
    ]:
        fig.add_annotation(
            x=x,
            y=0.98,
            text=f"<b>{label}</b>",
            showarrow=False,
            align="center",
            font=dict(size=11, color=color)
        )

    # outer=(lim+MDC95)/2
    # for x,label,color in [
    #     (-outer,"&gt; Measurement variability<br>(decreased stiffness)","#d85b2f"),
    #     (0,"Within measurement variability","#00765d"),
    #     (outer,"&gt; Measurement variability<br>(increased stiffness)","#d85b2f")
    # ]:
    #     fig.add_annotation(x=x,y=0.98,text=label,showarrow=False,
    #                        align="center",font=dict(size=12,color=color))
        
    # Marker, short vertical stem and a green/amber floating label.
    fig.add_shape(type="line",x0=adjusted,x1=adjusted,y0=0,y1=0.52,
                  line=dict(color=accent,width=2.5))
    fig.add_trace(go.Scatter(x=[adjusted],y=[0],mode="markers",
        marker=dict(size=19,color=accent,line=dict(color="white",width=3)),
        hovertemplate="Adjusted SWE change: %{x:+.2f} kPa<extra></extra>",
        showlegend=False))
    fig.add_annotation(x=adjusted,y=0.57,text=f"<b>{adjusted:+.2f} kPa</b>",
                       showarrow=False,yanchor="bottom",bgcolor=accent,
                       font=dict(size=13,color="white"),borderpad=6)
    fig.update_layout(height=255,margin=dict(l=5,r=5,t=4,b=4),
        paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans",color="#526a87"),showlegend=False,
        xaxis=dict(range=[-lim-.5,lim+.5],visible=False,fixedrange=True),
        yaxis=dict(range=[-.58,1.27],visible=False,fixedrange=True))
    st.plotly_chart(fig,use_container_width=True,
                    config={"displayModeBar":False,"staticPlot":True})

    st.markdown(
        """
        <div style="
            display:flex;
            justify-content:center;
            gap:18px;
            flex-wrap:wrap;
            font-size:0.78rem;
            color:#6d83a2;
            margin-top:-10px;
            margin-bottom:14px;
            text-align:center;
        ">
            <span>↓ Decreased stiffness</span>
            <span>● Within measurement variability</span>
            <span>↑ Increased stiffness</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # st.markdown(
    #     "<div style='text-align:center;color:#6d83a2;font-size:.86rem;margin-top:-16px;margin-bottom:18px'>Bias-adjusted longitudinal change (kPa)</div>",
    #     unsafe_allow_html=True
    # )
    
    if exceeds:
        st.markdown("""
        <div style="
            background-color:#fff0e8;
            border:1px solid #f4c9b5;
            border-left:4px solid #df663c;
            border-radius:12px;
            padding:16px 20px;
            color:#a94727;
            line-height:1.6;
        ">
            <strong>Change exceeds estimated measurement variability.</strong>
            The bias-adjusted change is outside the study-derived
            MDC95 limits. This change does not necessarily indicate fibrosis progression or regression.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="
            background-color:#dcf5e9;
            border:1px solid #b9e6d0;
            border-left:4px solid #09865e;
            border-radius:12px;
            padding:16px 20px;
            color:#08724f;
            line-height:1.6;
        ">
            <strong>Change within estimated measurement variability.</strong>
            The bias-adjusted change does not exceed the
            study-derived MDC95; a true longitudinal change
            cannot be reliably distinguished from measurement
            variability using this threshold.
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        "<div style='height: 24px;'></div>",
        unsafe_allow_html=True
    )

with st.expander("▦ Calculation methodology"):
    st.latex(r"\Delta_{\mathrm{adjusted}}=(SWE_{\mathrm{followup}}-SWE_{\mathrm{baseline}})-(\beta_{\mathrm{followup}}-\beta_{\mathrm{baseline}})")
    st.markdown("**Model-estimated SWE differences by vendor and transducer**")
    model_table = pd.DataFrame([
        {"Vendor": "GE", "Transducer": "Curvilinear", "Estimated mean difference* (kPa)": "Reference", "95% CI": "—", "p": "—"},
        {"Vendor": "GE", "Transducer": "Linear", "Estimated mean difference* (kPa)": "+2.14", "95% CI": "+1.33 to +2.95", "p": "< .001"},
        {"Vendor": "Siemens", "Transducer": "Curvilinear", "Estimated mean difference* (kPa)": "−2.72", "95% CI": "−3.03 to −2.42", "p": "< .001"},
        {"Vendor": "SuperSonic", "Transducer": "Curvilinear", "Estimated mean difference* (kPa)": "−0.42", "95% CI": "−0.75 to −0.09", "p": "0.014"},
        {"Vendor": "SuperSonic", "Transducer": "Linear", "Estimated mean difference* (kPa)": "+0.48†", "95% CI": "−0.13 to +1.09", "p": "0.12"},
    ])
    st.dataframe(
        model_table,
        hide_index=True,
        use_container_width=True,
        column_config={
            "Vendor": st.column_config.TextColumn("Vendor"),
            "Transducer": st.column_config.TextColumn("Transducer"),
            "Estimated mean difference* (kPa)": st.column_config.TextColumn("Estimated mean difference* (kPa)"),
            "95% CI": st.column_config.TextColumn("95% CI"),
            "p": st.column_config.TextColumn("p"),
        },
    )
    st.caption(
    "*Differences relative to GE with a curvilinear transducer.  \n"
    "†Derived estimate incorporating the vendor–transducer interaction."
    )

with st.expander("⚠ Important limitations"):
    st.markdown("""
    - **Research use only:** This calculator is a research prototype
      and has not been externally validated for clinical decision-making.

    - **Measurement range:** The adjustment coefficients and MDC95 were derived from measurements ≤15 kPa; applicability beyond this range has not been established.

    - **Equipment applicability:** The adjustment coefficients were
      derived from five ultrasound system–transducer combinations:
      GE C1–6, GE L2–9, Siemens 9C2, SuperSonic XC6–1,
      and SuperSonic SL10–2.
    """)

st.markdown(
    """
    <div class='footnote'>
        Liver SWE Change Calculator · v0.3 · Research use only
        <div style='margin-top:5px;'>
            Department of Radiology, Severance Hospital,
            Yonsei University College of Medicine
        </div>
        <div style='margin-top:5px;'>
            Study reference: Publication pending
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
