# Read a file when only the file name is known
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import pymysql
import pandas as pd
import textwrap

# Load API key from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Set up OpenAI client
client = OpenAI(api_key=api_key)
file=input("enter the file name whose code you want to understand >")
file_name = file # Replace this with your actual file name
user_prompt = ''

try:
    with open(file_name, 'r') as file:
        content = file.read()
        print("=== File Content ===")
        # print(content)  # Optional: show the file content
        user_prompt = f"{user_prompt}{content}"  # Correct string concatenation
except FileNotFoundError:
    print(f"File '{file_name}' not found.")
except Exception as e:
    print(f"An error occurred: {e}")  # Fixed syntax error here

input_example="""
import conf from '../conf/conf.js';
import { Client, Account } from "appwrite";

class AuthService {
    constructor() {
        if (!AuthService.instance) {
            this.client = new Client();
            this.account = new Account(this.client);

            this.client
                .setEndpoint(conf.appwriteUrl)
                .setProject(conf.appwriteProjectId);

            AuthService.instance = this;
        }

        return AuthService.instance;
    }

    async createAccount({ email, password, name }) {
        try {
            const userId = this.generateValidUserId();
            const userAccount = await this.account.create(userId, email, password, name);
            if (userAccount) {
                console.log("Account created successfully, attempting to login...");
                return this.login({ email, password });
            } else {
                return userAccount;
            }
        } catch (error) {
            console.error("Error creating account:", error);
            throw error;
        }
    }

    generateValidUserId() {
        const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
        let userId = '';
        for (let i = 0; i < 36; i++) {
            userId += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        return userId;
    }

    async login({ email, password }) {
        try {
            const session = await this.account.createEmailPasswordSession(email, password);
            console.log("Login successful:", session);
            return session;
        } catch (error) {
            console.error("Error logging in:", error);
            throw error;
        }
    }

    async getCurrentUser() {
        try {
            const user = await this.account.get();
            console.log("Current user:", user);
            return user;
        } catch (error) {
            console.error("Error fetching current user:", error);
        }

        return null;
    }

    async logout() {
        try {
            await this.account.deleteSessions();
            console.log("Logout successful");
        } catch (error) {
            console.error("Error logging out:", error);
        }
    }
}

const authService = new AuthService();
Object.freeze(authService); // Ensures the singleton pattern

export default authService;
"""

output_example="""
import conf from '../conf/conf.js';
import { Client, Account } from "appwrite";

conf: Contains environment-specific configuration like Appwrite URL and project ID.

{ Client, Account }: Imported from Appwrite SDK — Client manages the API connection, Account manages user-related operations (create, login, etc.).

➤ Class Declaration

class AuthService {
Defines a class AuthService that will contain methods for authentication.
➤ Singleton Constructor
    constructor() {
        if (!AuthService.instance) {
            this.client = new Client();
            this.account = new Account(this.client);

            this.client
                .setEndpoint(conf.appwriteUrl)
                .setProject(conf.appwriteProjectId);

            AuthService.instance = this;
        }

        return AuthService.instance;
    }
Singleton check: Ensures only one instance of AuthService is created. The first time the constructor is called:

this.client = new Client(): Initializes Appwrite client.

this.account = new Account(this.client): Creates an account object tied to the client.

.setEndpoint(...): Sets the Appwrite API URL.

.setProject(...): Sets the Project ID to scope all future calls.

💡 AuthService.instance = this saves the first instance. On subsequent new AuthService() calls, it just returns that saved instance.
➤ Method: createAccount
    async createAccount({ email, password, name }) {
Creates a new Appwrite user with the given email, password, and name.
        try {
            const userId = this.generateValidUserId();

            Generates a random 36-character ID manually. Appwrite normally auto-generates it, but you're customizing it.

            const userAccount = await this.account.create(userId, email, password, name);
Calls Appwrite’s account.create() method to register the user.
            if (userAccount) {
                console.log("Account created successfully, attempting to login...");
                return this.login({ email, password });
If account creation is successful, it automatically logs the user in.
            } else {
                return userAccount;
            }
If something unexpected happens, just return the userAccount response.
        } catch (error) {
            console.error("Error creating account:", error);
            throw error;
        }
Handles errors from Appwrite and throws them to the calling code.
➤ Method: generateValidUserId
    generateValidUserId() {
        const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
        let userId = '';
        for (let i = 0; i < 36; i++) {
            userId += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        return userId;
    }

    Generates a random 36-character alphanumeric string (A-Z, a-z, 0–9).

Used as a custom user ID.
➤ Method: login
    async login({ email, password }) {
        try {
            const session = await this.account.createEmailPasswordSession(email, password);
            console.log("Login successful:", session);
            return session;
        } catch (error) {
            console.error("Error logging in:", error);
            throw error;
        }
    }

    Uses Appwrite’s createEmailPasswordSession() to log in the user and start a session.

If successful, logs and returns the session object.
➤ Method: getCurrentUser
    async getCurrentUser() {
        try {
            const user = await this.account.get();
            console.log("Current user:", user);
            return user;
        } catch (error) {
            console.error("Error fetching current user:", error);
        }

        return null;
    }
Calls Appwrite’s account.get() to fetch the currently logged-in user's data.

Returns user info or null if not logged in.
➤ Method: logout
    async logout() {
        try {
            await this.account.deleteSessions();
            console.log("Logout successful");
        } catch (error) {
            console.error("Error logging out:", error);
        }
    }

    Deletes all active sessions for the user (i.e., logs them out everywhere).
    ➤ Export the Singleton
    const authService = new AuthService();
Object.freeze(authService); // Ensures the singleton pattern

export default authService;

Creates a single frozen instance of AuthService, ensuring no further modifications or re-instantiations.

Exports it so you can use it anywhere in your app like:

"""

system_prompt=f'''
You are a coding expert. The user will provide a **code file** as input.

🎯 Your job is to go through the code **line by line** and explain each line **in simple, clear terms**.

📌 Your response MUST follow this exact **JSON list format**:
[
  {{ "line": "<exact code line>", "explanation": "<clear and simple explanation of that line>" }},
  ...
]

💡 Rules to follow:
1. 🔹 Include EVERY line — code, imports, comments, blank lines, brackets.
2. 🔹 Do NOT combine multiple lines. Each line = one object.
3. 🔹 Do NOT summarize or skip — explain everything line-by-line.
4. 🔹 Keep explanations beginner-friendly but accurate.
5. 🔹 Keep JSON properly formatted — no syntax issues.

🔄 Workflow steps:
You must always follow this exact 5-step process in order:
- "analyse": Briefly describe what the user wants.
- "think": Explain your strategy to fulfill the request.
- "output": Return a JSON array as explained above.
- "validate": Confirm your output matches the expected structure.
- "result": State the final result of your analysis.

⚠️ Format your entire response strictly as:

{{"step":"<step_name>", "content":<step_description_or_json_array>}}

example:
input:
{input_example}
output:
{{step:"analayse",content:"alright user is interested to know the explanation of each and every line in the code }}
{{step:"think",content:"to perform that i must go through the code from top to bottom analyse the code and convey the meaning of each and every line to him"}}
{{step:"output",content:{output_example}}}
{{step:"validate",content:"seems like the generated response is correct output for this"}}
{{step:"result",content:"The required content has been generated by analysing the code from top to bottom"}}
'''

messages=[]
messages.append({"role":"system","content":system_prompt})
messages.append({"role":"user","content":user_prompt})
while True:
    res=client.chat.completions.create(
            model="gpt-4o",
            response_format={"type":"json_object"},
            messages=messages
        )
    parsed_response=json.loads(res.choices[0].message.content)
    print(parsed_response)
    if(parsed_response.get("step")!="result"):
        messages.append({"role":"assistant","content":json.dumps(parsed_response)})
        continue
    else:
         messages.append({"role":"assistant","content":json.dumps(parsed_response)})
         break
    
output=messages[-3]["content"]
output=json.loads(output)
output = output['content'] 
if isinstance(output, str):
 output = json.loads(output) # This should be a list of dicts
 
# Get base file name
base_name = os.path.splitext(file_name)[0]  # removes .py
output_file = base_name + ".md"

# Format each line beautifully in Markdown
formatted_blocks = []
for i, item in enumerate(output):
    code_line = item.get("line", "").strip()
    explanation = item.get("explanation", "").strip()

    block = f"""
---

### 🔹 Line {i + 1}

{code_line}



📖 **Explanation**:
{explanation}
"""
    formatted_blocks.append(block)

# Combine all blocks into one markdown text
final_markdown = "\n".join(formatted_blocks)

# Save the markdown content to a file
with open(output_file, "w", encoding="utf-8") as f:
    f.write(final_markdown)

print(f"✅ Content saved to {output_file}")
