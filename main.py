import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from PIL import Image
import os

# 🌟 Set Beautiful Theme & Layout
st.set_page_config(page_title="CHRISPO '25 Analysis", page_icon="🏆", layout="wide")

# 🎨 Custom CSS for Beautiful UI
st.markdown("""
    <style>
        body {
            background-color: #f5f7fa;
            color: #333;
        }
        .css-18e3th9 {
            background-color: #f0f2f6;
        }
        .css-1d391kg {
            background-color: #fff;
        }
        .stButton>button {
            background-color: #ff6f61;
            color: white;
            border-radius: 10px;
            padding: 10px;
            font-size: 16px;
        }
        h1 {
            color: #ff6f61;
        }
    </style>
""", unsafe_allow_html=True)

# 🎯 Generate Dataset
def generate_dataset():
    np.random.seed(42)
    sports = ["Football", "Basketball", "Tennis", "Badminton", "Cricket", 
              "Volleyball", "Hockey", "Table Tennis", "Swimming", "Athletics"]
    colleges = ["College A", "College B", "College C", "College D", "College E"]
    states = ["Karnataka", "Tamil Nadu", "Kerala", "Maharashtra", "Telangana"]
    
    data = {
        "Participant_ID": range(1, 301),
        "Name": [f"Player {i}" for i in range(1, 301)],
        "Sport": np.random.choice(sports, 300),
        "College": np.random.choice(colleges, 300),
        "State": np.random.choice(states, 300),
        "Day": np.random.randint(1, 6, 300),
        "Age": np.random.randint(18, 30, 300),
        "Gender": np.random.choice(["Male", "Female", "Other"], 300),
        "Score": np.random.randint(1, 100, 300),
        "Feedback": np.random.choice(["Great event!", "Loved it!", "Needs improvement!", "Amazing experience!"], 300),
    }

    df = pd.DataFrame(data)
    df.to_csv("participants.csv", index=False)
    return df

# 📊 Load or Generate Dataset
if not os.path.exists("participants.csv"):
    df = generate_dataset()
else:
    df = pd.read_csv("participants.csv")

# 🏆 App Title
st.title("🏆 CHRISPO '25 Tournament Analysis by TUSHAR MAHAJAN | 3 MCA A | 2447156")

# 🎛️ Sidebar Filters
st.sidebar.header("🎯 Filter Data")
selected_sport = st.sidebar.selectbox("Select Sport", ["All"] + list(df["Sport"].unique()))
selected_college = st.sidebar.selectbox("Select College", ["All"] + list(df["College"].unique()))
selected_state = st.sidebar.selectbox("Select State", ["All"] + list(df["State"].unique()))

# 🔍 Apply Filters
filtered_df = df.copy()
if selected_sport != "All":
    filtered_df = filtered_df[filtered_df["Sport"] == selected_sport]
if selected_college != "All":
    filtered_df = filtered_df[filtered_df["College"] == selected_college]
if selected_state != "All":
    filtered_df = filtered_df[filtered_df["State"] == selected_state]

st.write("### 📊 Filtered Participation Data")
st.dataframe(filtered_df.style.set_properties(**{'background-color': '#f8f9fa', 'color': 'black'}))

# 📈 Participation Trends
st.write("## 📈 Participation Trends")

# 🎨 Modern Colors
sns.set_palette("coolwarm")

# 1️⃣ Bar Chart: Sports-wise Participation
st.write("### 🎯 Sports-wise Participation")
fig1, ax1 = plt.subplots(figsize=(8, 4))
sns.countplot(x="Sport", data=df, order=df["Sport"].value_counts().index, ax=ax1, palette="pastel")
ax1.set_title("Sports-wise Participation")
ax1.tick_params(axis='x', rotation=45)
st.pyplot(fig1)

# 2️⃣ Line Chart: Day-wise Participation
st.write("### 📅 Day-wise Participation")
daywise_count = df["Day"].value_counts().sort_index()
fig2, ax2 = plt.subplots(figsize=(8, 4))
ax2.plot(daywise_count.index, daywise_count.values, marker='o', linestyle='-', color='#007bff', linewidth=2)
ax2.set_title("Participation Trend Over Days", fontsize=14, color="#007bff")
ax2.set_xlabel("Day", fontsize=12)
ax2.set_ylabel("Number of Participants", fontsize=12)
st.pyplot(fig2)

# 3️⃣ Pie Chart: College-wise Participation
st.write("### 🎓 College-wise Participation")
college_counts = df["College"].value_counts()
fig3, ax3 = plt.subplots(figsize=(6, 6))
ax3.pie(college_counts, labels=college_counts.index, autopct='%1.1f%%', colors=sns.color_palette("coolwarm", len(college_counts)))
ax3.set_title("College-wise Participation Distribution", fontsize=14, color="#d9534f")
st.pyplot(fig3)

# 4️⃣ Stacked Area Chart: State-wise Participation
st.write("### 🌍 State-wise Participation")
statewise_data = df.groupby(["Day", "State"]).size().unstack().fillna(0)
fig4, ax4 = plt.subplots(figsize=(8, 4))
statewise_data.plot(kind="area", stacked=True, colormap="coolwarm", alpha=0.7, ax=ax4)
ax4.set_title("State-wise Participation Over Days", fontsize=14, color="#5bc0de")
ax4.set_xlabel("Day", fontsize=12)
ax4.set_ylabel("Number of Participants", fontsize=12)
st.pyplot(fig4)

# 🌟 Word Cloud for Feedback
st.write("## 💬 Participant Feedback - Word Cloud")
all_feedback = " ".join(df["Feedback"])
wordcloud = WordCloud(width=800, height=400, background_color="white", colormap="coolwarm").generate(all_feedback)
fig_wc, ax_wc = plt.subplots(figsize=(8, 4))
ax_wc.imshow(wordcloud, interpolation="bilinear")
ax_wc.axis("off")
st.pyplot(fig_wc)

# 🏅 Image Processing
st.write("## 🏅 Sports Image Gallery")
image_folder = "images/"  
if os.path.exists(image_folder):
    image_files = os.listdir(image_folder)
    selected_image = st.selectbox("Choose an image to process", image_files)
    img = Image.open(os.path.join(image_folder, selected_image))
    
    # Show Original Image
    st.image(img, caption="Original Image", use_column_width=True)

    # Convert Image to Grayscale
    gray_img = img.convert("L")
    st.image(gray_img, caption="Grayscale Image", use_column_width=True)

else:
    st.write("No images found! Please add images to the 'images/' folder.")

# 🎯 Summary
st.write("### 🎯 Summary")
st.write("- The dashboard provides insights into sports participation trends.")
st.write("- Word Cloud gives an overview of participant feedback.")
st.write("- Image processing module allows viewing and modifying sports-related images.")

st.success("✅ CHRISPO '25 Analysis Completed Successfully!")
st.success("ETE - 3 | Advanced Python Programming | Made By: Tushar Mahajan")
