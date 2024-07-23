import joblib
import pandas as pd
import gradio as gr


credit_score_scaling = data = joblib.load('models/credit_score_scaling.joblib')


def predict_credit_score(
    person_age,
    person_income,
    person_home_ownership,
    person_emp_length,
    loan_intent,
    loan_grade,
    loan_amnt,
    loan_int_rate,
    loan_percent_income,
    cb_person_default_on_file,
    cb_person_cred_hist_length,
):
    input_df = pd.DataFrame(
        {
            "person_age": [person_age],
            "person_income": [person_income],
            "person_home_ownership": [person_home_ownership],
            "person_emp_length": [person_emp_length],
            "loan_intent": [loan_intent],
            "loan_grade": [loan_grade],
            "loan_amnt": [loan_amnt],
            "loan_int_rate": [loan_int_rate],
            "loan_percent_income": [loan_percent_income],
            "cb_person_default_on_file": [cb_person_default_on_file],
            "cb_person_cred_hist_length": [cb_person_cred_hist_length],
        }
    )
    credit_scores_df = credit_score_scaling.calculate_credit_score(input_df.copy(deep=False))
    return int(credit_scores_df["credit_score"][0])


inputs = [
    gr.Number(label="Person Age", minimum=18, value=25, step=1),
    gr.Number(label="Person Annual Income (USD)", minimum=0.0, value=50_000.0, step=1000.0),
    gr.Radio(label="Home Ownership", choices=["RENT", "OWN", "MORTGAGE", "OTHER"]),
    gr.Number(label="Employment Length (Years)", minimum=0.0, maximum=50.0, value=5.0, step=1.0),
    gr.Dropdown(
        label="Loan Intent",
        choices=["PERSONAL", "EDUCATION", "HOMEIMPROVEMENT", "DEBTCONSOLIDATION", "BUSINESS", "MEDICAL", "OTHER"]
    ),
    gr.Dropdown(label="Loan Grade", choices=["A", "B", "C", "D", "E", "F", "G"]),
    gr.Number(label="Loan Amount (USD)", minimum=0, value=10000, step=500),
    gr.Number(label="Interest Rate (%)", minimum=0.0, maximum=100.0, value=10.0, step=0.1),
    gr.Number(
        label="Loan Amount as Percentage of Income",
        minimum=0.0,
        maximum=1.0,
        value=0.0,
        step=0.01
    ),
    gr.Radio(label="Default on File", choices=["Y", "N"]),
    gr.Number(label="Credit History Length (Years)", minimum=0, value=10, step=1)
]

outputs = ["number"]

examples = [
    [27,34000,"OWN",7.0,"EDUCATION","C",8000,12.53,0.24,"N",10],
    [36,45600,"MORTGAGE",8.0,"MEDICAL","A",18000,6.91,0.39,"N",11],
    [33,75000,"MORTGAGE",2.0,"DEBTCONSOLIDATION","B",7500,10.08,0.1,"N",9],
    [24,79632,"RENT",0.0,"EDUCATION","C",25000,13.35,0.31,"N",4],
]


title = "Credit Score App"
description = "Enter the details of the loan applicant?"
article = "This app is a part of my credit-score-modelling project from GitHub which can be access through https://github.com/marcellinus-witarsah/credit-score-modelling"


gr.Interface(
    fn=predict_credit_score,
    inputs=inputs,
    outputs=outputs,
    examples=examples,
    title=title,
    description=description,
    article=article,
    theme=gr.themes.Soft(),
).launch()

# if __name__ == "__main__":
#     person_age = 27
#     person_income = 56525
#     person_home_ownership = "MORTGAGE"
#     person_emp_length = 4.0
#     loan_intent = "MEDICAL"
#     loan_grade = "D"
#     loan_amnt = 12000
#     loan_int_rate = 15.95
#     loan_percent_income = 0.18
#     cb_person_default_on_file = "N"
#     cb_person_cred_hist_length = 10
#     print("Credit Score: {}".format(predict_credit_score(
#         person_age=person_age,
#         person_income=person_income,
#         person_home_ownership=person_home_ownership,
#         person_emp_length=person_emp_length,
#         loan_intent=loan_intent,
#         loan_grade=loan_grade,
#         loan_amnt=loan_amnt,
#         loan_int_rate=loan_int_rate,
#         loan_percent_income=loan_percent_income,
#         cb_person_default_on_file=cb_person_default_on_file,
#         cb_person_cred_hist_length=cb_person_cred_hist_length,
#     )))
