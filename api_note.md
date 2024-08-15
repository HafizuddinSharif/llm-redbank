## GET "/isready"

To check if chatbot is ready to start chat
**response:**

```
{
    "success": true,
    "message": "Chatbot is ready"
}
```

## POST "/start-chat"

To start the chatbot. This API require to supply the brn number to get the appropiate ctos data
**request**

```
{
    brn: "12345F"
}
```

**response**

```
{
    "success": true,
    "response": "...."
}
```

## POST "/chat"

To continue chatting with the chatbot. POST "/start-chat" should be called first before this.
**request:**

```
{
    query: "12345F"
}
```

**response:**

```
{
    "success": true
    "response": "...."
}
```
