import jieba
import fasttext
from flask import Flask, render_template, request

app = Flask(__name__)
classifier = fasttext.load_model("model/Intelligent_Guidance/model.bin")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    input_line = " ".join( list( jieba.cut(userText) ) )
    response = classifier.predict([input_line])[0][0][0]
    recommend_keshi = response[response.find("__label__")+len("__label__"):] 
    return "推荐您到: "+ recommend_keshi + "，点击[挂号]，一键直达。"


if __name__ == "__main__":
    app.run()
