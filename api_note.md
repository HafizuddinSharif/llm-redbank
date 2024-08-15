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
    "input": true,
    "chat_history": [
        {
            "content": "...",
            "type": "human",
            // there's more but not important
        }
    ],
    "context": [
        {
            "id": 1,
            metadata: { source: "/document.md" },
            "page_content": "...",
            "type": "Document"
        }
    ],
    "answer": "..."
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
    "input": true,
    "chat_history": [
        {
            "content": "...",
            "type": "human",
            // there's more but not important
        }
    ],
    "context": [
        {
            "id": 1,
            metadata: { source: "/document.md" },
            "page_content": "...",
            "type": "Document"
        }
    ],
    "answer": "..."
}
```
