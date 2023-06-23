from flask import Flask, request,json

app = Flask(__name__)
@app.route('/example', methods=['POST'])
def handle_json():
  content_type = request.headers.get('Content-Type')
  print(content_type)
  
  if request.is_json:
    data = request.json
    items = data['items']

    for item in items:
        price = item['salePrice']
        name = item['name']
        print (price)
        print (name)
  else:
    print("Not a JSON")

  return "message"
    #return render_template('index.html')
if __name__ == '__main__':
    app.run()