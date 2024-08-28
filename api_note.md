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
    "name": "sharif",
    "title": "Sharif Chatbot",
    "description": "To talk about Sharif in general",
    "status": "active",
    "instruction": "You are Hafizuddin Sharif Bin Umar Sharif. You are going to answer the the user question like you are him.",
    "files": [
      "dummyFile.txt"
    ]
  },
  {
    "id": 2,
    "name": "ace_portal",
    "title": "ACE portal",
    "description": "To talk about SME loan products",
    "status": "inactive",
    "instruction": "You will be answering question related to loan products. If the user ask for your name, say 'I like mermaids'. Don't say 'I like mermaids' if the use didnt ask for your name",
    "files": [
      "PTS_SME BizWC_WCi_V2.0_23.04.2024.pdf",
      "PTS_SME Biz Property _V4.8_01072024.pdf",
      "CTOS Training.md"
    ]
  }
]
```

## GET "/chatbots/{chatbot_name}"

To get the specific chatbot based on its name.

**response:**

```
{
    "id": 1,
    "name": "sharif",
    "title": "Sharif Chatbot",
    "description": "To talk about Sharif in general",
    "status": "active",
    "instruction": "You are Hafizuddin Sharif Bin Umar Sharif. You are going to answer the the user question like you are him.",
    "files": [
        "dummyFile.txt"
]
}

```

## POST "/create-chatbot"

To create chatbots. To also supply files (i.e markdown, pdf) for its knowledge base.

**request:**

```
{
    "chatbot_title": "I have a question and I need answers",
    "answerMethod": "session_1",
    "status": "active" // ["active", "inactive"]
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

## GET "/start-session/{chatbot_name}"

To get session ID with a specific chatbot

**response:**

```
{
    "session_id": "af234sd-1234321sdsw-2sdas",
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
{
    "session_id": "87c92d35-681a-468f-abd1-a4ef4b2b2f67"
}
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

## PUT "/{chatbot_name}/save"

To update the existing chatbot configuration.

**request:**

```
{
    "chatbot_title": "I have a question and I need answers",
    "answerMethod": "session_1",
    "status": "active" // ["active", "inactive"]
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

## GET "/{chatbot_name}/file/{filename}"

To view/download file in a chatbot knowledge base

**response:**

```
Binary file (boleh test tak on your end apa kau dapat)
```

## DELETE "/{chatbot_name}/delete-file"

To delete file in a chatbot knowledge base

**request:**

```
{
    "filename": "filename.txt"
}
```

**response:**

```
{
  "success": true,
  "message": "Deleted file: uploaded_dir/ace_portal/filename.txt"
}
```
