from flask import Flask,render_template,request
from src.pipeline.predict_pipeline import CustomData,PredictPipeline

application=Flask(__name__) # entry point
app=application

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predictdata',methods=['GET','POST'])
def predict_datapoint():
    if request.method=='GET':
        return render_template('home.html')
    
    else:
        data=CustomData(gender=request.form.get('gender'),race_ethnicity=request.form.get('race_ethnicity'),parental_level_of_education=request.form.get('parental_level_of_education'),
                        lunch=request.form.get('lunch'),test_preparation_course=request.form.get('test_preparation_course'),reading_score=request.form.get('reading_score'),writing_score=request.form.get('writing_score'))
        
        pred_df=data.get_data_as_dataFrame()
        print(pred_df)

        predict_pipeline=PredictPipeline()
        predicted_result=predict_pipeline.predict(pred_df)

        return render_template('home.html',results=predicted_result[0])
    """✅ Why [0] is used
            Because:
            👉 predicted_result is usually a NumPy array or list
            👉 Even when you predict one row, sklearn returns:

            array([123.45])
            not:
            123.45
            So:
            predicted_result[0]
            means:
            ➡️ Take the first (and only) value from that array."""
                

if __name__=="__main__" :
    app.run(debug=True, use_reloader=False, port=8000)



