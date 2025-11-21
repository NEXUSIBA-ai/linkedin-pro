import streamlit as st
import openai
import os
from dotenv import load_dotenv
load_dotenv()

# === CONFIG ===
client = openai.OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

st.set_page_config(page_title="LinkedIn Pro", page_icon="🚀")
st.title("🚀 Générateur de Posts LinkedIn qui Cartonnent (Freelances & Devs)")

# === STRIPE PAYMENT ===
import stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

price_id = "price_1..."  # ← tu mettras ton vrai Price ID après création (2 clics)

if "paid" not in st.session_state:
    st.session_state.paid = False

if not st.session_state.paid:
    st.warning("Accès unique : 19 € (paiement 100% sécurisé)")
    if st.button("💳 Payer 19 € et débloquer l'outil illimité"):
        checkout_session = stripe.checkout.sessions.create(
            payment_method_types=['card'],
            line_items=[{'price': price_id, 'quantity': 1}],
            mode='payment',
            success_url=st.secrets["SUCCESS_URL"] + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=st.secrets["CANCEL_URL"],
        )
        st.markdown(f'<script src="https://js.stripe.com/v3/"></script><script>var stripe = Stripe("{st.secrets["STRIPE_PUBLISHABLE_KEY"]}"); stripe.redirectToCheckout({{sessionId: "{checkout_session.id}"}});</script>', unsafe_allow_html=True)
else:
    st.success("✅ Accès débloqué à vie !")

    nom = st.text_input("Ton prénom (ex: Kevin)")
    job = st.text_input("Ton job / expertise (ex: Développeur Fullstack, Growth Hacker, Copywriter)")
    cible = st.text_input("Ta cible (ex: startups SaaS, entrepreneurs 30-45 ans, boîtes e-commerce)")
    ton_style = st.selectbox("Ton style habituel", ["Pro & classe", "Cash & direct", "Fun & authentique", "Inspirant & motivant"])

    if st.button("Générer 5 posts LinkedIn qui cartonnent"):
        if not nom or not job or not cible:
            st.error("Remplis tous les champs stp")
        else:
            with st.spinner("Génération en cours... (5-8 secondes)"):
                prompt = f"""
                Tu es un expert LinkedIn qui fait +1000 likes par post.
                Écris 5 posts LinkedIn différents (entre 80 et 220 mots chacun) pour {nom}, {job}.
                Cible : {cible}.
                Style : {ton_style.lower()}.
                Chaque post doit avoir :
                - Un accroche ultra-puissante dès la 1ère ligne
                - Une histoire ou exemple concret
                - Une leçon claire
                - Un call-to-action naturel (commenter, DM, etc.)
                Varier les formats : question, histoire perso, chiffre choc, fail, conseil actionnable.
                Émojis pertinents, sauts de ligne parfaits, ton humain et zéro bullshit corporate.
                """

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.8,
                    max_tokens=4096
                )
                posts = response.choices[0].message.content.strip().split("\n\n")

                for i, post in enumerate(posts[:5], 1):
                    st.markdown(f"### Post {i} 🚀")
                    st.write(post)
                    st.markdown("---")
