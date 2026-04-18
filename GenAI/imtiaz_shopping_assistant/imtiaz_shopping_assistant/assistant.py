import pandas as pd
import streamlit as st
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

st.set_page_config(page_title="Imtiaz Superstore AI Assistant", layout="centered")
st.title("Imtiaz Superstore AI Assistant")

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat history
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.write(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.write(msg.content)

# Load product and user data
products_df = pd.read_excel("imtiaz_superstore_products.xlsx")
with open("users_data.json") as f:
    users_data = json.load(f)["users"]

# Define tools
@tool
def get_product_info(product_name: str = None, product_id: str = None, brand: str = None, category: str = None, sub_category: str = None, min_price: float = None, max_price: float = None, tags: str = None) -> str:
    """
    Fetch detailed product information from the superstore database based on dynamic filters.

    This tool allows filtering products by name, ID, brand, category, subcategory, price range, and tags.
    It respects the capitalization of the data in the spreadsheet and returns formatted product details.

    Args:
        product_name (str, optional): Name of the product to search for.
        product_id (str, optional): Unique ID of the product.
        brand (str, optional): Brand name of the product.
        category (str, optional): Main category of the product.
        sub_category (str, optional): Subcategory of the product.
        min_price (float, optional): Minimum price filter (inclusive).
        max_price (float, optional): Maximum price filter (inclusive).
        tags (str, optional): Search for products containing these tags (case-insensitive).

    Returns:
        str: A string listing all matching products with detailed information including:
             - ID, Name, Brand, Category, Subcategory
             - Price in PKR, Stock, Discount %, Halal, Organic, Imported
             - Tags, Popularity Score, Rating
             If no products match the criteria, returns a user-friendly message.

    Example:
        >>> get_product_info(product_name="Y80 Ultra 8 in 1 smartwatch")
        'ID: P001, Name: Y80 Ultra 8 In 1 Smartwatch, Brand: XYZ, Category: Electronics, ...'
    """
    df = products_df.copy()

    def title_case(val):
        return val.title() if isinstance(val, str) else val

    if product_name:
        df = df[df["product_name"] == title_case(product_name)]
    if product_id:
        df = df[df["product_id"] == product_id]
    if brand:
        df = df[df["brand"] == title_case(brand)]
    if category:
        df = df[df["category"] == title_case(category)]
    if sub_category:
        df = df[df["sub_category"] == title_case(sub_category)]
    if min_price is not None:
        df = df[df["price_pkr"] >= min_price]
    if max_price is not None:
        df = df[df["price_pkr"] <= max_price]
    if tags:
        df = df[df["tags"].str.contains(tags, case=False, na=False)]

    if df.empty:
        return "No products match the given criteria."

    results = []
    for _, row in df.iterrows():
        results.append(f"ID: {row['product_id']}, Name: {row['product_name']}, Brand: {row['brand']}, Category: {row['category']}, Subcategory: {row['sub_category']}, Price: {row['price_pkr']} PKR, Stock: {row['stock']}, Discount: {row['discount_percent']}%, Halal: {row['halal_certified']}, Organic: {row['organic']}, Imported: {row['imported']}, Tags: {row['tags']}, Popularity: {row['popularity_score']}, Rating: {row['rating']}")
    return "\n".join(results)

@tool
def get_user_data(user_id: str) -> dict:
    """
    Retrieve a full user profile from the database, including loyalty points, tier, and personal information.

    This tool searches the JSON-based user database for a user by their unique ID and returns all associated data.
    It can be used to check loyalty points, purchase history, or other account details.

    Args:
        user_id (str): The unique identifier of the user in the database.

    Returns:
        dict: A dictionary containing the user's data. Example fields include:
              - 'user_id': str
              - 'name': str
              - 'email': str
              - 'phone': str
              - 'loyalty_points': int
              - 'tier': str
              - 'purchase_history': list
              If the user is not found, returns:
              {'error': 'User not found.'}

    Example:
        >>> get_user_data("U001")
        {'user_id': 'U001', 'name': 'Ali Khan', 'email': 'ali@example.com', 'loyalty_points': 120, 'tier': 'Gold', ...}
    """
    user = next((u for u in users_data if u["user_id"] == user_id), None)
    if not user:
        return {"error": "User not found."}
    return user

@tool
def calculate_final_price(price: float, loyalty_points: int) -> str:
    """
    Calculate the final payable price of a product after applying loyalty points as a discount.

    The tool ensures that the discount applied does not exceed the product price.
    It is used to determine the effective cost for the user after redeeming loyalty points.

    Args:
        price (float): The original price of the product in PKR.
        loyalty_points (int): The number of loyalty points to apply as a discount.

    Returns:
        str: A human-readable string showing:
             - Discount applied in PKR
             - Final price after applying the discount

    Example:
        >>> calculate_final_price(5000, 200)
        'Discount applied: 200 PKR. Final price: 4800 PKR.'
        >>> calculate_final_price(300, 500)
        'Discount applied: 300 PKR. Final price: 0 PKR.'
    """
    discount = min(price, loyalty_points)
    final_price = price - discount
    return f"Discount applied: {discount} PKR. Final price: {final_price} PKR."

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools([get_product_info, get_user_data, calculate_final_price])

# Workflow executor
def execute_workflow(query: str) -> str:
    st.session_state.messages.append(HumanMessage(content=query))

    response = llm_with_tools.invoke(st.session_state.messages)

    tool_results = []
    if hasattr(response, "tool_calls") and response.tool_calls:
        for tool_call in response.tool_calls:
            result = ""
            if tool_call["name"] == "get_product_info":
                result = get_product_info.invoke(tool_call).content
            elif tool_call["name"] == "get_user_data":
                result = get_user_data.invoke(tool_call).content
            elif tool_call["name"] == "calculate_final_price":
                result = calculate_final_price.invoke(tool_call).content
            tool_results.append(f"{tool_call['name']} output: {result}")

    combined_context = query
    if tool_results:
        combined_context += "\n\nTool Results:\n" + "\n".join(tool_results)

    final_response = llm_with_tools.invoke([HumanMessage(content=combined_context)]).content
    st.session_state.messages.append(AIMessage(content=final_response))

    return final_response

# UI
user_input = st.chat_input("Enter your query")
if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    result = execute_workflow(user_input)

    with st.chat_message("assistant"):
        st.write(result)
