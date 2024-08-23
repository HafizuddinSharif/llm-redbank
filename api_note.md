## GET "/isready"

To check if chatbot is ready to start chat
**response:**

```
{
    "success": true,
    "message": "Chatbot is ready"
}
```

## POST "/start-chat/{chatbot_name}"

To start the chatbot. This API require to supply the brn number to get the appropiate ctos data
**request**

```
{
    "brn": "12345F"
}
```

**response**

```
{
    "input": "This is where the user question will be shown",
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
    "answer": "...",
    "session_id": "session_1"
}
```

## POST "/chat/{chatbot_name}"

To continue chatting with the chatbot. POST "/start-chat/{chatbot_name}" should be called first before this.
**request:**

```
{
    "query": "I have a question and I need answers",
    "session_id": "session_1"
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

## POST "/send-brn"

FE to send-brn to BE to create the session

**request:**

```
{
    "brn":"1408874K"
}
```

**response:**

```
[
    "session created with session_id: d8709baa-dd5d-4082-941a-df623da4051a"
]
```


## POST "/askMe"

FE to send query with session_id

**request:**

```
{
    "query": "what is the total revenue, profit before tax and total asset for this data?",
    "session_id": "9236bb6e-953f-459a-a08b-db8c478dbadd"
}
```

**response:**

```
[
    "askMe successful"
]
```