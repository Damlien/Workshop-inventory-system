from flask import Flask, render_template_string, request
from inventory_service import get_inventory, search_item

app = Flask(__name__)  #creates the flask application

@app.route("/")  #connects the home URL (/) to a function

def data_retrival():

    user_input = request.args.get("search") 

    if user_input:
        inventory_data = search_item(user_input)
    else:
        inventory_data =get_inventory()

    # <h1> </h1> header 1 , <table> </table> table
    html_design = """
    <h1> My Inventory </h1>  
    """


    html_design +="""
    <form>
        <input type="text" name="search" placeholder="Search..." >
        <button>Search</button>
    </form>
    """
    #opening table tag
    html_design += """
    <table border="1">  
    """
    #+= adds more text to variable, <tr> </tr> table row, <th> </th> table header
    html_design += """
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Quantity</th>
            <th>Shelf</th>
        </tr>
    """
    # {% for i in items %} loop, {% endfor %} ends loop, <td> </td> table data
    html_design += """
        {% for items in in_storage %}  

        <tr>
            <td> {{items.id}} </td>
            <td> {{items.name}} </td>
            <td> {{items.quantity}} </td>
            <td> {{items.shelf}} </td>
        </tr>
        {% endfor %}
    """
    #closing table tag
    html_design += """
    </table>
    """ 
   
  

    return render_template_string(html_design, in_storage =inventory_data)



if __name__ == "__main__":
    app.run(debug=True)