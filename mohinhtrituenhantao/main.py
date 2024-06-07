from flask import Flask, render_template, request #render_template dùng để render template HTML
import openai
from rapidfuzz import fuzz
import json
app = Flask(__name__)

# Cài đặt thông tin model
model = "gpt-3.5-turbo-0125"
with open("apikey.txt","r") as f:
    openai.api_key = f.readline()
# Đọc tập dữ liệu JSON
with open("data.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

# Hàm để gọi đến OpenAI / ChatGPT hoặc tập dữ liệu JSON (tùy chọn)
def get_response(user_question):
    # Tìm câu hỏi tương tự nhất trong tập dữ liệu
    max_similarity = 0
    best_question = None
    for question in dataset.keys():
        similarity = fuzz.ratio(user_question.lower(), question.lower())
        if similarity > max_similarity:
            max_similarity = similarity
            best_question = question

    if max_similarity > 50:  # Điều chỉnh ngưỡng tương tự tùy ý
        return dataset[best_question]
    else:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": user_question}],
            max_tokens=1024,
            temperature=0.5
        )
        response_text = response.choices[0].message['content']
        return response_text
@app.route('/', methods=['POST', 'GET']) # được thiết lập để xử lý 2 yêu cầu post và get
def hello():
    # dùng lệnh request để bắn post lên
    # Chuỗi nội dung chat hiện tại
    noidungchathientai = ""

    if request.method == "GET":
        return render_template('base.html', noidungchathientai=noidungchathientai)
    else:
        # Lấy tin nhắn từ form
        user_message = request.form['user_message']
        noidungchathientai += "\n[BẠN]:" + user_message

        # Gọi hàm để lấy phản hồi từ OpenAI hoặc ChatGPT
        bot_response = get_response(user_message)
        noidungchathientai += "\n[BOT]:" + bot_response

        return render_template('base.html', noidungchathientai=noidungchathientai)

# Thực thi server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
