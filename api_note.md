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
    "query": "what is the total revenue in 2021, total revenue in 2020 and total revenue in 2022 and the sum of it for this data?",
    "session_id": "141ab35a-f5fe-4e14-8f5e-1053f830fa7d"
}
```

**response:**

```
{
    "141ab35a-f5fe-4e14-8f5e-1053f830fa7d": "The total revenue for 2022 was RM 1,483,001.00, 2021 was RM 1,320,508.00 and 2020 was RM 1,149,104.00.  The sum of the total revenue for these years is RM 4,052,613.00. \n"
}
```

## POST "/bubble"

FE to send predefined bubble query with session_id

**request:**

```
{
    "query": "redflags",
    "session_id": "141ab35a-f5fe-4e14-8f5e-1053f830fa7d"
}
```

**response:**

```
{
    "d44bfc1a-3638-49ef-ab99-457f0bc0270a": {
        "both_brankrupt": "The customer and its related parties have bankruptcy records. Please perform your due diligence and proceed with caution.",
        "customer_bankrupt": "The customer has a bankruptcy record. Please perform your due diligence and proceed with caution.",
        "customer_related_brankrupt": "<#>: The customer has related parties with a bankruptcy record. Please perform your due diligence and proceed with caution.",
        "gear_ratio": "The customer has a very high gearing ratio of <190.0/100>. Please look into the customer’s financial reports to perform your due diligence. You can ask me to retrieve any number of financial data available in the CTOS reports.",
        "profit_margin": "The customer had a very poor profit margin of <-4.0>. Please look into the customer’s financial reports to perform your due diligence. You can ask me to retrieve any number of financial data available in the CTOS reports.",
        "legal_status": "The customer has records of legal proceedings. In particular, with regards to <Summon/Writ files> on <02-04-2024>.",
        "msic_code": "The customer operates in a high risk industry code: <63910>.",
        "trex_ref": "The customer has records of negative non-bank monthly payment(s) (such as, but not limited to: rental, telco and utilities bill payments). As such, please perform due diligence.",
        "age_of_company": "The customer’s age is too young, at only <282> days old."
    }
}
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
