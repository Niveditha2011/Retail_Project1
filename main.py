import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mysql.connector

connection = mysql.connector.connect(
  host = "gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
  port = 4000,
  user = "2XWsHPpwQA4Z6ce.root",
  password = "lFu7DqRUZThvq3kn",
  database = "Retail_Project",
 
)
mycursor=connection.cursor()

df = pd.read_csv("orders.csv")
#Divided data into two two dataframe
df1 = df[['order_id', 'order_date', 'ship_mode','segment','country','city','state','postal_code','region','category','sub_category']]  # First half of columns
df2 = df[['order_id','product_id','cost_price','list_price','quantity','discount_percent','discount','sale_price','profit']]

user_color='#154360'
original_title = """
<div style="background-color:{};padding:12px">
<h2 style="font-family:Courier;color:white;font-weight: bold;test-align:center;">📊 RETAIL ORDER DATA-WEB APP</h2>
</div>""".format(user_color)
st.markdown(original_title, unsafe_allow_html=True)


ques_options = ["select a Question", 
            "1. Find top 10 highest revenue generating products",
            "2. Find the top 5 cities with the highest profit margins",
            "3. Calculate the total discount given for each category",
            "4. Find the average sale price per product category",
            "5. Find the region with the highest average sale price",
            "6. Find the total profit per category",
            "7. Identify the top 3 segments with the highest quantity of orders",
            "8. Determine the average discount percentage given per region",
            "9. Find the product category with the highest total profit",
            "10. Calculate the total revenue generated per year",
            "11. List all Product category and its avg profit",
            "12. Total sale price per each sub category",
            "13. Identify the top 3 category with the highest quantity of orders",
            "14. Count of top 10 total products from each city",
            "15. Calculate Total discount percent per sub category",
            "16. Top 10 region wise highest sold products",
            "17. United States in kentucky state how many furniture sold",
            "18. Find the Profit percentage per Sub_Category",
            "19. Determine the average discount given per country in consumer segment",
            "20. List Top 10 highest order placed city"]

st.sidebar.image(r"C:\Users\Python Class\Retail_Project\image\download.jpg")
sel_option = st.sidebar.selectbox("SQL QUESTIONS",ques_options,index=0) 

#1
if sel_option == "1. Find top 10 highest revenue generating products":
    mycursor.execute("""
    SELECT product_id, SUM(sale_price * quantity) AS total_revenue
    FROM RETAIL_PROJECT.orders_table
    GROUP BY product_id
    ORDER BY total_revenue DESC
    LIMIT 10
    """) 
    result = mycursor.fetchall()
    # Convert to DataFrame
    df = pd.DataFrame(result, columns=["Product Id", "Total Revenue"])
    # Display Data
    st.write("### Top 10 Revenue-Generating Products")
    st.dataframe(df)
    chart_data = pd.DataFrame(df, columns=["Product Id", "Total Revenue"]).set_index("Product Id")
    #button to generate plot
    if st.sidebar.button("Generate plot"):
        fig, ax = plt.subplots(figsize=(6,4))
        st.bar_chart(chart_data)
    
#2
elif sel_option == '2. Find the top 5 cities with the highest profit margins':
    mycursor.execute(
    """SELECT city,(SUM(profit) / SUM(sale_price * quantity)) * 100 AS profit_margin
       FROM RETAIL_PROJECT.orders_table 
       GROUP BY city
       ORDER BY profit_margin DESC 
       LIMIT 5 """)
    result = mycursor.fetchall()
    df = pd.DataFrame(result, columns=["City", "Profit_Margin"])
    st.write("### Top 5 Cities with Highest Profit Margins")
    st.dataframe(df)
    chart_data = pd.DataFrame(df, columns=["City", "Profit_Margin"]).set_index("City")
    if st.sidebar.button("Generate plot"):
        fig, ax = plt.subplots(figsize=(6,4))
        #st.bar_chart(chart_data)
        ax.plot(df["City"], df["Profit_Margin"], marker='o', linestyle='-')
        ax.set_xlabel("City")
        ax.set_ylabel("Profit_Margin")
        ax.set_title("Top 5 Cities with Highest Profit Margins")
        plt.xticks(rotation=45)
        st.pyplot(fig)
        

#3
elif sel_option == '3. Calculate the total discount given for each category':
    mycursor.execute(
    """SELECT category,SUM(discount*quantity) AS total_discount 
       FROM RETAIL_PROJECT.orders_table 
       GROUP BY category
       ORDER BY total_discount DESC""")
    result = mycursor.fetchall()
    df = pd.DataFrame(result, columns=["Product Category", "Total Discount"])
    st.write("### Total Discount given for each Category")
    st.dataframe(df)
    chart_data = pd.DataFrame(df, columns=["Product Category", "Total Discount"]).set_index("Product Category")
    #button to generate plot
    if st.sidebar.button("Generate plot"):
        fig, ax = plt.subplots(figsize=(6,4))
        st.bar_chart(chart_data)

#4
elif sel_option == '4. Find the average sale price per product category':
    mycursor.execute(
    """SELECT category,AVG(sale_price) AS avg_saleprice 
    FROM RETAIL_PROJECT.orders_table 
    GROUP BY category
    ORDER BY avg_saleprice DESC""")
    result = mycursor.fetchall()
    df = pd.DataFrame(result, columns=["Product Category", "Average Sale Price"])
    st.write("### Average sale price per Product Category")
    st.dataframe(df)
    chart_data = pd.DataFrame(df, columns=["Product Category", "Average Sale Price"]).set_index("Product Category")
    if st.sidebar.button("Generate plot"):
        fig, ax = plt.subplots(figsize=(6,4))
        #st.bar_chart(chart_data)
        ax.plot(df["Product Category"], df["Average Sale Price"], marker='o', linestyle='-')
        ax.set_xlabel("Product Category")
        ax.set_ylabel("Average Sale Price")
        ax.set_title("Average sale price per Product Category")
        plt.xticks(rotation=45)
        st.pyplot(fig)

#5
elif sel_option == '5. Find the region with the highest average sale price':
    mycursor.execute(
    """SELECT region ,AVG(sale_price) as avg_saleprice
    FROM RETAIL_PROJECT.orders_table 
    GROUP BY region 
    ORDER BY avg_saleprice DESC 
    LIMIT 1""")
    result = mycursor.fetchall()
    df = pd.DataFrame(result, columns=["Region", "Average Sale Price"])
    st.write("### Region with the highest average sale price")
    st.dataframe(df)

#6
elif sel_option == '6. Find the total profit per category':
    mycursor.execute(
    """SELECT category,SUM(profit) AS Total_profit 
    FROM RETAIL_PROJECT.orders_table 
    GROUP BY category
    ORDER BY Total_profit DESC """)
    result = mycursor.fetchall()
    df = pd.DataFrame(result, columns=["Product Category", "Total Profit"])
    st.write("### Total profit per Category")
    st.dataframe(df)
    chart_data = pd.DataFrame(df, columns=["Product Category", "Total Profit"]).set_index("Product Category")
    #button to generate plot
    if st.sidebar.button("Generate plot"):
        fig, ax = plt.subplots(figsize=(6,4))
        st.bar_chart(chart_data)
    
#7
elif sel_option == '7. Identify the top 3 segments with the highest quantity of orders':
    mycursor.execute(
    """SELECT segment,SUM(quantity) AS Total_quantity 
    FROM RETAIL_PROJECT.orders_table 
    GROUP BY segment 
    ORDER BY Total_quantity DESC 
    LIMIT 3  """)
    result = mycursor.fetchall()
    df = pd.DataFrame(result, columns=["Segment", "Total Quantity"])
    st.write("### Identify the top 3 segments with the highest quantity of orders")
    st.dataframe(df)
    chart_data = pd.DataFrame(df, columns=["Segment", "Total Quantity"]).set_index("Total Quantity")
    #button to generate plot
    if st.sidebar.button("Generate plot"):
        fig, ax = plt.subplots(figsize=(6,4))
        st.bar_chart(chart_data)

#8
elif sel_option == '8. Determine the average discount percentage given per region':
    mycursor.execute(
    """SELECT region,AVG(discount_percent) AS AVERAGE_DISCOUNT
    FROM RETAIL_PROJECT.orders_table 
    GROUP BY region 
    ORDER BY AVERAGE_DISCOUNT DESC""")
    result = mycursor.fetchall()
    df = pd.DataFrame(result, columns=["Region", "AVG_Discount_Percent"])
    st.write("### Average discount percentage given per region")
    st.dataframe(df)
    chart_data = pd.DataFrame(df, columns=["Region", "AVG_Discount_Percent"]).set_index("Region")
    if st.sidebar.button("Generate plot"):
        fig, ax = plt.subplots(figsize=(6,4))
        #st.bar_chart(chart_data)
        ax.plot(df["Region"], df["AVG_Discount_Percent"], marker='o', linestyle='-')
        ax.set_xlabel("Region")
        ax.set_ylabel("AVG_Discount_Percent")
        ax.set_title("Average discount percentage given per region")
        plt.xticks(rotation=45)
        st.pyplot(fig)

#9
elif sel_option == '9. Find the product category with the highest total profit':
    mycursor.execute(
    """SELECT category ,SUM(profit) AS Total_Profit
    FROM RETAIL_PROJECT.orders_table 
    GROUP BY category 
    ORDER BY Total_Profit DESC LIMIT 1  """)
    result = mycursor.fetchall()
    df = pd.DataFrame(result, columns=["Product Category", "Total Profit"])
    st.write("### Product Category with the Highest Total Profit")
    st.dataframe(df)

#10
elif sel_option == '10. Calculate the total revenue generated per year':
    mycursor.execute(
    """SELECT YEAR(order_date) AS year,SUM(sale_price) AS total_revenue 
    FROM RETAIL_PROJECT.orders_table 
    GROUP BY YEAR(order_date) 
    ORDER BY year """ )
    result = mycursor.fetchall()
    df = pd.DataFrame(result, columns=["Year", "Total Revenue"])
    st.write("### Total Revenue generated Per Year")
    st.dataframe(df)
    chart_data = pd.DataFrame(df, columns=["Year", "Total Revenue"]).set_index("Year")
    #button to generate plot
    if st.sidebar.button("Generate plot"):
        fig, ax = plt.subplots(figsize=(6,4))
        st.bar_chart(chart_data)

#11
elif sel_option == '11. List all Product category and its avg profit':
    mycursor.execute(
        """SELECT df1.category, AVG(df2.profit) AS avg_profit
        FROM RETAIL_PROJECT.ORDER1 df1
        JOIN RETAIL_PROJECT.ORDER2 df2 ON df1.order_id = df2.order_id
        GROUP BY df1.category
        ORDER BY avg_profit DESC""")
    result = mycursor.fetchall()  
    df = pd.DataFrame(result, columns=["Product Category", "Avg Profit"])
    st.write("### List of Product Categories and Their Average Profit")
    st.dataframe(df)

#12 
elif sel_option == '12. Total sale price per each sub category':
    mycursor.execute(
        """SELECT df1.sub_category, SUM(df2.sale_price) AS total_saleprice
        FROM RETAIL_PROJECT.ORDER1 df1
        JOIN RETAIL_PROJECT.ORDER2 df2 ON df1.order_id = df2.order_id
        GROUP BY df1.sub_category
        ORDER BY total_saleprice DESC""")
    result = mycursor.fetchall()  
    df = pd.DataFrame(result, columns=["Product Sub-Category", "Total SalePrice"])
    st.write("### Total sale price per each sub category")
    st.dataframe(df)
    
    chart_data = pd.DataFrame(df, columns=["Product Sub-Category", "Total SalePrice"]).set_index("Product Sub-Category")
    if st.sidebar.button("Generate plot"):
        fig, ax = plt.subplots(figsize=(6,4))
        #st.bar_chart(chart_data)
        ax.plot(df["Product Sub-Category"], df["Total SalePrice"], marker='o', linestyle='-')
        ax.set_xlabel("Product Sub-Category")
        ax.set_ylabel("Total SalePrice")
        ax.set_title("Total sale price per each sub category")
        plt.xticks(rotation=45)
        st.pyplot(fig)

#13
elif sel_option == '13. Identify the top 3 category with the highest quantity of orders':
    mycursor.execute(
        """SELECT df1.category, SUM(df2.quantity) AS quantity
        FROM RETAIL_PROJECT.ORDER1 df1
        JOIN RETAIL_PROJECT.ORDER2 df2 ON df1.order_id = df2.order_id
        GROUP BY df1.category
        ORDER BY quantity DESC
        LIMIT 3""")
    result = mycursor.fetchall()  
    df = pd.DataFrame(result, columns=["Product Sub-Category", "Total Price"])
    st.write("### Top 3 category with the highest quantity of orders")
    st.dataframe(df)

#14
elif sel_option == '14. Count of top 10 total products from each city':
    mycursor.execute(
        """SELECT df1.city, COUNT(df2.product_id) AS total_products
        FROM RETAIL_PROJECT.ORDER1 df1
        INNER JOIN RETAIL_PROJECT.ORDER2 df2 ON df1.order_id = df2.order_id
        GROUP BY df1.city
        ORDER BY total_products DESC
        LIMIT 10""")
    result = mycursor.fetchall()  
    df = pd.DataFrame(result, columns=["City", "Total Product"])
    st.write('### Top 10 total products from each city')
    st.dataframe(df)
    chart_data = pd.DataFrame(df, columns=["City", "Total Product"]).set_index("City")
    if st.sidebar.button("Generate plot"):
        st.bar_chart(chart_data)

#15
elif sel_option == '15. Calculate Total discount percent per sub category':
    mycursor.execute(
        """SELECT df1.sub_category, SUM(df2.discount_percent) AS discount_percent
        FROM RETAIL_PROJECT.ORDER1 df1
        JOIN RETAIL_PROJECT.ORDER2 df2 ON df1.order_id = df2.order_id
        GROUP BY df1.sub_category
        ORDER BY discount_percent DESC""")
    result = mycursor.fetchall()  
    df = pd.DataFrame(result, columns=["Sub Category", "Total discount"])
    st.write('### Total discount percent per sub category')
    st.dataframe(df)

    chart_data = pd.DataFrame(df, columns=["Sub Category", "Total discount"]).set_index("Sub Category")
    if st.sidebar.button("Generate plot"):
        fig, ax = plt.subplots(figsize=(6,4))
        ax.plot(df["Sub Category"], df["Total discount"], marker='o', linestyle='-')
        ax.set_xlabel("Sub Category")
        ax.set_ylabel("Total discount")
        ax.set_title("Total discount percent per sub category")
        plt.xticks(rotation=45)
        st.pyplot(fig)


#16  
elif sel_option == '16. Top 10 region wise highest sold products':
    mycursor.execute(
        """SELECT df2.product_id,df1.region, SUM(df2.quantity) AS TOTAL_QUANTITY
        FROM RETAIL_PROJECT.ORDER1 df1
        LEFT JOIN RETAIL_PROJECT.ORDER2 df2 ON df1.order_id = df2.order_id
        GROUP BY df1.region,df2.product_id
        ORDER BY TOTAL_QUANTITY DESC
        LIMIT 10""")
    result = mycursor.fetchall()  
    df = pd.DataFrame(result, columns=["Product Id", "Region","TOTAL_QUANTITY"])
    st.write('### Top 10 region wise highest sold products')
    st.dataframe(df)

    chart_data = pd.DataFrame(df, columns=["Product Id", "TOTAL_QUANTITY"]).set_index("Product Id")
    if st.sidebar.button("Generate plot"):
        fig, ax = plt.subplots(figsize=(6,4))
        ax.plot(df["Product Id"], df["TOTAL_QUANTITY"], marker='o', linestyle='-')
        ax.set_xlabel("Product Id")
        ax.set_ylabel("TOTAL_QUANTITY")
        ax.set_title("Top 10 region wise highest sold products")
        plt.xticks(rotation=45)
        st.pyplot(fig)

#17  
elif sel_option == '17. United States in kentucky state how many furniture sold':
    mycursor.execute(
        """SELECT df1.country,df1.state,df1.category,SUM(df2.quantity) AS TOTAL_QUATITY
        FROM RETAIL_PROJECT.ORDER1 df1
        JOIN RETAIL_PROJECT.ORDER2 df2 ON df1.order_id = df2.order_id
        WHERE df1.country="United States" and df1.state="Kentucky" and df1.category="Furniture"     
        GROUP BY df1.country,df1.state,df1.category
        """)
    result = mycursor.fetchall()  
    df = pd.DataFrame(result, columns=["Country", "State","Furniture","TOTAL_QUATITY"])
    st.write('### United States in Kentucky State total Furniture sold')
    st.dataframe(df)

#18
elif sel_option == '18. Find the Profit percentage per Sub_Category':
    mycursor.execute(
        """SELECT df1.sub_category,SUM(df2.profit) AS Total_Profit
        FROM RETAIL_PROJECT.ORDER1 df1
        JOIN RETAIL_PROJECT.ORDER2 df2 ON df1.order_id = df2.order_id   
        GROUP BY df1.sub_category
        ORDER BY Total_Profit DESC
        """)
    result = mycursor.fetchall()  
    df = pd.DataFrame(result, columns=["Sub_Category","Total_Profit"])
    st.write('### Profit percentage per Sub_Category')
    st.dataframe(df)
    chart_data = pd.DataFrame(df, columns=["Sub_Category", "Total_Profit"]).set_index("Sub_Category")
    if st.sidebar.button("Generate plot"):
        st.bar_chart(chart_data)

#19
elif sel_option == '19. Determine the average discount given per country in consumer segment':
    mycursor.execute(
        """SELECT df1.segment,df1.country,AVG(df2.discount) AS Discount
        FROM RETAIL_PROJECT.ORDER1 df1
        INNER JOIN RETAIL_PROJECT.ORDER2 df2 ON df1.order_id = df2.order_id  
        WHERE df1.segment="Consumer"
        GROUP BY df1.country
        ORDER BY Discount DESC
        """)
    result = mycursor.fetchall()  
    df = pd.DataFrame(result, columns=["Segment","Country","Discount"])
    st.write('### Average discount given per country in consumer segment')
    st.dataframe(df)

#20
elif sel_option == '20. List Top 10 highest order placed city':
    mycursor.execute(
        """SELECT df1.city,SUM(df2.quantity) AS Total_Quantity
        FROM RETAIL_PROJECT.ORDER1 df1
        JOIN RETAIL_PROJECT.ORDER2 df2 ON df1.order_id = df2.order_id   
        GROUP BY df1.city
        ORDER BY Total_Quantity DESC
        LIMIT 10""")
    result = mycursor.fetchall()  
    df = pd.DataFrame(result, columns=["City","Total_Quantity"])
    st.write('### Top 10 highest order placed city')
    st.dataframe(df)
    chart_data = pd.DataFrame(df, columns=["City","Total_Quantity"]).set_index("City")
    if st.sidebar.button("Generate plot"):
        fig, ax = plt.subplots(figsize=(6,4))
        ax.plot(df["City"], df["Total_Quantity"], marker='o', linestyle='-')
        ax.set_xlabel("City")
        ax.set_ylabel("Total_Quantity")
        ax.set_title("Top 10 highest order placed city")
        plt.xticks(rotation=45)
        st.pyplot(fig)

