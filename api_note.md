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

To start the chatbot. This will return the answer for the query and the session id. Make sure in your request payload the `session_id` is empty

**request**

```
{
    "query": "This is the first question",
    "session_id": ""
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

To continue chatting with the chatbot. POST `/start-chat/{chatbot_name}` should be called first before this. session_id should
be supplied from POST `/start-chat/{chatbot_name}` response payload.

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

## GET "/chatbots"

To get the list of chatbots.

**response:**

```
[
    {
        "id": 1,
        "name": "ace_portal",
        "title": "ACE portal",
        "status": "active",
        "instruction": "You will be answering question related to loan products. If the user ask for your name, say 'I like mermaids'. Don't say 'I like mermaids' if the use didnt ask for your name"
    },
    {
        "id": 2,
        "name": "sme_products",
        "title": "SME Loan Products Chatbot",
        "status": "inactive"
    }
]
```

## POST "/{chatbot_name}/save"

To create/update chatbots. To also supply files (i.e markdown, pdf) for its knowledge base.

**request:**

```
{
    "chatbot_title": "I have a question and I need answers",
    "answerMethod": "session_1",
    "files": [] // Ni aku tak tahu macam mana hahahaha
}
```

**response:**

```
{
    "info": "5 files successfully uploaded!",
    "files": ""
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
