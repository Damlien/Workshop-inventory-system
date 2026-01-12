import streamlit as st
import pandas as pd
from inventory_service import get_inventory, new_item, change_stock, update_item

# --- CONFIGURATION ---
st.set_page_config(layout="wide", page_title="Workshop System")

# --- INITIALIZATION ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
if "selected_id" not in st.session_state:
    st.session_state.selected_id = None # Tracks which item is open on the right

# ==========================================
# 1. LOGIN SCREEN (Identical logic to your Tkinter)
# ==========================================
if not st.session_state.logged_in:
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        st.title("🔐 Login")
        
        tab1, tab2 = st.tabs(["Store Worker", "Administrator"])
        
        with tab1:
            if st.button("Log in as Worker", use_container_width=True):
                st.session_state.logged_in = True
                st.session_state.is_admin = False
                st.rerun()
        
        with tab2:
            pwd = st.text_input("Password", type="password")
            if st.button("Log in as Admin", use_container_width=True):
                if pwd == "1234":
                    st.session_state.logged_in = True
                    st.session_state.is_admin = True
                    st.rerun()
                else:
                    st.error("Wrong password")
    st.stop()

# ==========================================
# 2. MAIN LAYOUT (Split View)
# ==========================================

# Header
col_head, col_out = st.columns([8, 1])
role = "ADMINISTRATOR" if st.session_state.is_admin else "Store Worker"
col_head.title(f"Inventory - {role}")
if col_out.button("Log Out"):
    st.session_state.logged_in = False
    st.session_state.selected_id = None
    st.rerun()

st.divider()

# Create the Split: Left (List) vs Right (Details)
# Tkinter: self.split_view = tk.PanedWindow...
col_left, col_right = st.columns([1, 2], gap="medium")

# Load Data
inventory = get_inventory()

# ==========================================
# 3. LEFT SIDE: THE LIST (Master)
# ==========================================
with col_left:
    st.subheader("Inventory List")
    
    # Search Bar
    search = st.text_input("🔍 Search", placeholder="Type to filter...", label_visibility="collapsed")
    
    # Filter Logic
    filtered_items = []
    if search:
        search_lower = search.lower()
        for item in inventory:
            if search_lower in item["name"].lower() or search_lower in str(item["id"]):
                filtered_items.append(item)
    else:
        filtered_items = inventory

    # THE SCROLLABLE LIST CONTAINER
    # This mimics the Tkinter Treeview area. 
    # We use a fixed height (500px) so it scrolls internally.
    with st.container(height=600, border=True):
        
        # We loop through items and create a BUTTON for each.
        # This removes the "checkbox" entirely. You just click the text.
        for item in filtered_items:
            # Determine if this button is "active" (selected)
            is_active = (st.session_state.selected_id == item["id"])
            
            # Label format: "Name (ID)"
            label = f"{item['name']} (ID: {item['id']})"
            
            # Logic: If clicked, update session state and rerun
            # type="primary" highlights the button if it's currently selected
            if st.button(label, key=f"btn_{item['id']}", use_container_width=True, type="primary" if is_active else "secondary"):
                st.session_state.selected_id = item["id"]
                st.rerun()

    # Admin: New Item Button (at bottom of list)
    if st.session_state.is_admin:
        st.write("")
        if st.button("➕ Register New Item", use_container_width=True):
            @st.dialog("Register New Item")
            def create_dialog():
                with st.form("create"):
                    n_name = st.text_input("Name")
                    n_id = st.number_input("ID", step=1, min_value=1)
                    n_qty = st.number_input("Qty", step=1, min_value=0)
                    n_shelf = st.text_input("Shelf")
                    if st.form_submit_button("Save"):
                        new_item(n_name, int(n_id), int(n_qty), n_shelf)
                        st.rerun()
            create_dialog()

# ==========================================
# 4. RIGHT SIDE: DETAILS (Detail)
# ==========================================
with col_right:
    # Check if an item is selected
    if st.session_state.selected_id is not None:
        # Find the specific item data
        selected_item = next((i for i in inventory if i["id"] == st.session_state.selected_id), None)
        
        if selected_item:
            # --- SHOW DETAILS ---
            with st.container(border=True):
                # Header
                st.markdown(f"## {selected_item['name']}")
                
                # Info Grid
                c_id, c_shelf = st.columns(2)
                c_id.metric("ID", selected_item["id"])
                c_shelf.metric("Location", selected_item.get("shelf", "-"))
                
                st.divider()
                
                # --- STOCK CONTROL (Big Buttons) ---
                st.subheader("Manage Stock")
                
                col_minus, col_display, col_plus = st.columns([1, 1, 1])
                
                with col_minus:
                    if st.button("➖ 1", use_container_width=True):
                        change_stock(selected_item["id"], -1)
                        st.rerun()
                    if st.button("➖ 5", use_container_width=True):
                        change_stock(selected_item["id"], -5)
                        st.rerun()

                with col_display:
                    # Big centered number
                    st.markdown(
                        f"<h1 style='text-align: center; margin: 0; font-size: 4rem;'>{selected_item['quantity']}</h1>", 
                        unsafe_allow_html=True
                    )
                    st.markdown("<p style='text-align: center; color: gray;'>In Stock</p>", unsafe_allow_html=True)

                with col_plus:
                    if st.button("➕ 1", use_container_width=True):
                        change_stock(selected_item["id"], 1)
                        st.rerun()
                    if st.button("➕ 5", use_container_width=True):
                        change_stock(selected_item["id"], 5)
                        st.rerun()

            # --- ADMIN EDITING (Only if Admin) ---
            if st.session_state.is_admin:
                st.write("")
                with st.expander("🛠 Edit Item Details"):
                    with st.form("edit_form"):
                        new_name = st.text_input("Name", value=selected_item['name'])
                        new_shelf = st.text_input("Shelf", value=selected_item['shelf'])
                        # Hidden ID field (conceptually)
                        
                        if st.form_submit_button("Save Changes"):
                            update_item(
                                selected_item["id"], 
                                selected_item["id"], 
                                new_name, 
                                selected_item["quantity"], 
                                new_shelf
                            )
                            st.success("Updated!")
                            st.rerun()
        else:
            st.warning("Item not found (it might have been deleted).")
            
    else:
        # Empty State (Matches your Tkinter "Select an item..." label)
        st.info("👈 Select an item from the list on the left to view details.")
        st.markdown(
            """
            <div style="text-align: center; opacity: 0.2; margin-top: 100px;">
                <span style="font-size: 5rem;">📦</span>
            </div>
            """, unsafe_allow_html=True
        )
        