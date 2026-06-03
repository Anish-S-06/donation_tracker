from app import create_app
from pyngrok import ngrok

app = create_app()


ngrok.set_auth_token("")

 # IMPORTANT: kill existing tunnels
ngrok.kill()

public_url = ngrok.connect(5000)
print("Public URL:", public_url)
app.config["DEBUG"]=True
if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

