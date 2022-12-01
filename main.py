import pandas as pd
import numpy as np
import streamlit as st
import cohere
import textwrap

def generate_question(inp_query):
    base_question_prompt = textwrap.dedent("""
    Given a paragraph, this program will generate questions from the paragraph.
    Paragraph: A declarative action model is a compact representation of the state transitions of dynamic systems that generalizes over world objects. The specification of declarative action models is often a complex hand-crafted task. In this paper we formulate declarative action models via state constraints, and present the learning of such models as a combinatorial search. The comprehensive framework presented here allows us to connect the learning of declarative action models to well-known problem solving tasks. In addition, our framework allows us to characterize the existing work in the literature according to four dimensions: (1) the target action models, in terms of the state transitions they define; (2) the available learning examples; (3) the functions used to guide the learning process, and to evaluate the quality of the learned action models; (4) the learning algorithm. Last, the paper lists relevant successful applications of the learning of declarative actions models and discusses some open challenges with the aim of encouraging future research work.
    Questions: What is a declarative action model? How does the framework mentioned help to characterize the existing work? What are some of the open challenges with respect to the successful applications of the learning of declarative actions models?
    
    --
    Paragraph:""")

    # Call the Cohere Generate endpoint
    response = co.generate(
        model='large',
        prompt=base_question_prompt + " " + inp_query + "\nQuestions:",
        max_tokens=150,
        temperature=0.7,
        k=0,
        p=0.7,
        frequency_penalty=0.1,
        presence_penalty=0,
        stop_sequences=["--"])

    questions = response.generations[0].text
    questions = questions.replace("\n\n--", "").replace("\n--", "").strip()

    return questions



API_KEY = 'j9fltyvpID3YyH82yoUqSCjhcydpMh1vG3lLS83z'
co = cohere.Client(API_KEY)

st.header('Questionaire')
st.subheader("It will generate a Question from Text that you Provide!")

response = "No Text submitted"

if 'response' not in st.session_state:
    st.session_state["response"] = response

with st.form('search_form'):
    inp_query = st.text_area('Enter Your Text', height=225)
    submitted = st.form_submit_button('Submit')

    if submitted:

        # response = co.generate(
        #     model='large',
        #     prompt=f'Given a paragraph, this program will generate questions from the paragraph.\n\nParagraph: A declarative action model is a compact representation of the state transitions of dynamic systems that generalizes over world objects. The specification of declarative action models is often a complex hand-crafted task. In this paper we formulate declarative action models via state constraints, and present the learning of such models as a combinatorial search. The comprehensive framework presented here allows us to connect the learning of declarative action models to well-known problem solving tasks. In addition, our framework allows us to characterize the existing work in the literature according to four dimensions: (1) the target action models, in terms of the state transitions they define; (2) the available learning examples; (3) the functions used to guide the learning process, and to evaluate the quality of the learned action models; (4) the learning algorithm. Last, the paper lists relevant successful applications of the learning of declarative actions models and discusses some open challenges with the aim of encouraging future research work.\nQuestions: What is a declarative action model? How does the framework mentioned help to characterize the existing work? What are some of the open challenges with respect to the successful applications of the learning of declarative actions models?\n--\nParagraph: {inp_query}\nQuestions:',
        #     max_tokens=150,
        #     temperature=0.7,
        #     k=0,
        #     p=1,
        #     frequency_penalty=0,
        #     presence_penalty=0,
        #     stop_sequences=["--"],
        #     return_likelihoods='NONE')
        #
        # response = response.generations[0].text
        # response = response.split("?")
        #
        # st.session_state["response"] = response

        response = [generate_question(inp_query).split("?") for _ in range(10)]
        # response = generate_question(inp_query)
        st.session_state["response"] = response

st.subheader("Question Generated From Text!")
st.write(st.session_state["response"])

# the sidebar gives 3 options to readers
# 1)to search for meaning internally
# 2)to generate keywords
with st.sidebar:
    option = st.selectbox(
        'Choose',
        ('Seek Clarification', 'Generate Keywords'))
    if option == "Seek Clarification":
        with st.form('clarification_form'):
            phrase = st.text_input('Phrase', "")
            context = st.text_input('Context', "")
            submitted = st.form_submit_button('Submit')
            if submitted:
                if len(phrase) == 0:
                    st.write("Enter phrase")
                elif len(context) == 0:
                    st.write("Enter context")
                else:

                    response = co.generate(
                        model='large',
                        prompt=f'Given a phrase and context, this program will generate explanation of the phrase in the given context. \n\nPhrase: Augmented reality\nContext: Artificial Intelligence\nExplanation: Augmented reality (AR) is an interactive experience that combines the real world and computer-generated content.The content can span multiple sensory modalities, including visual, auditory, haptic, somatosensory and olfactory.\n--\nPhrase: {phrase}\nContext: {context}\nExplanation:',
                        max_tokens=200,
                        temperature=0.5,
                        k=0,
                        p=1,
                        frequency_penalty=0.2,
                        presence_penalty=0.2,
                        stop_sequences=["--"],
                        return_likelihoods='NONE')
                    st.write(response.generations[0].text[0:-2])

    elif option == 'Generate Keywords':

        response = co.generate(
            model='large',
            prompt=f'Given a paragraph, this program will generate important keywords.\n\nParagraph: We study the computational complexity of abstract argumentation semantics based on weak admissibility, a recently introduced concept to deal with arguments of self-defeating nature. Our results reveal that semantics based on weak admissibility are of much higher complexity (under typical assumptions) compared to all argumentation semantics which have been analysed in terms of complexity so far. In fact, we show PSPACE-completeness of all non-trivial standard decision problems for weak-admissible based semantics. We then investigate potential tractable fragments and show that restricting the frameworks under consideration to certain graph-classes significantly reduces the complexity. We also show that weak-admissibility based extensions can be computed by dividing the given graph into its strongly connected components (SCCs). This technique ensures that the bottleneck when computing extensions is the size of the largest SCC instead of the size of the graph itself and therefore contributes to the search for fixed-parameter tractable implementations for reasoning with weak admissibility.\nKeywords: computational complexity, abstract argumentation semantics, PSPACE-completeness, weak-admissible based semantics\n--\nParagraph: A declarative action model is a compact representation of the state transitions of dynamic systems that generalizes over world objects. The specification of declarative action models is often a complex hand-crafted task. In this paper we formulate declarative action models via state constraints, and present the learning of such models as a combinatorial search. The comprehensive framework presented here allows us to connect the learning of declarative action models to well-known problem solving tasks. In addition, our framework allows us to characterize the existing work in the literature according to four dimensions: (1) the target action models, in terms of the state transitions they define; (2) the available learning examples; (3) the functions used to guide the learning process, and to evaluate the quality of the learned action models; (4) the learning algorithm. Last, the paper lists relevant successful applications of the learning of declarative actions models and discusses some open challenges with the aim of encouraging future research work.\nKeywords: declarative action model, state constraints, combinatorial search\n--\nParagraph: {inp_query}\nKeywords:',
            max_tokens=15,
            temperature=0.5,
            k=0,
            p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop_sequences=["--"],
            return_likelihoods='NONE')
        st.write(response.generations[0].text)
