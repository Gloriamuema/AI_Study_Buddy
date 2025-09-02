# Register
curl -X POST http://127.0.0.1:5000/register \
-H "Content-Type: application/json" \
-d '{"username":"testuser","password":"1234"}'

# Login
curl -X POST http://127.0.0.1:5000/login \
-H "Content-Type: application/json" \
-d '{"username":"testuser","password":"1234"}'
