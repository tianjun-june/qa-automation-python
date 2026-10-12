import time

from playwright.sync_api import Page, expect

def test_drag_and_drop(page: Page):
    page.set_content("""
    <style>
        #source {
        display: inline-block;
        padding: 12px;
        border: 1px solid gray;
        cursor: grab;
        }
        
        #target {
        margin-top: 20px;
        min-height: 100px;
        padding: 16px;
        border: 2px dashed gray;
        }
    </style>
    <div id="source" draggable="true">
        Order #123
    </div>
    
    <div id="target">
        Drop order here
    </div>
    
    <p id="status">Waiting</p>
    
    <script>
        const source = document.querySelector("#source");
        const target = document.querySelector("#target");
        
        source.addEventListener("dragstart", event => {
            event.dataTransfer.setData(
            "text/plain", "Order #123");
            });
            
            target.addEventListener("dragover", event => {
                event.preventDefault();
                });
                
            target.addEventListener("drop", event => {
                event.preventDefault();
                
                const order = event.dataTransfer.getData(
                "text/plain");
                
                target.appendChild(source);
                
                document.querySelector("#status").textContent = "Received: " + order;
            });
    </script>
    """)

    source =  page.locator("#source")
    target = page.locator("#target")
    source.drag_to(target)

    expect(
        page.locator("#status")
    ).to_have_text("Received: Order #123")

    expect(
        target.locator("#source")
    ).to_have_text("Order #123")


def test_keyboard_shortcuts(page: Page):
    page.set_content("""
    <label for="notes">Order notes</label>
    <input id="notes">
    
    <p id="result">Not submitted</p>
    
    <script>
        document.querySelector("#notes")
            .addEventListener("keydown", event => {
                if (event.key === "Enter") {
                document.querySelector("#result")
                    .textContent = " Submitted: " + event.target.value;
                }
            });
    </script>
    """)

    notes = page.get_by_role("textbox", name="Order notes")

    notes.fill("Draft order")
    time.sleep(2)
    # Select all existing text
    notes.press("ControlOrMeta+A")
    time.sleep(2)
    # Replace selected text by typing
    notes.press_sequentially("Final order")
    time.sleep(2)
    expect(notes).to_have_value("Final order")

    # Submit using Enter
    notes.press("Enter")
    time.sleep(2)
    expect(
        page.locator("#result")
    ).to_have_text("Submitted: Final order")

def test_mouse_interactions(page: Page):
    page.set_content("""
    <button id="menu">Actions</button>
    <div id="panel" hidden>Advanced options</div>
    
    <button id="order">Double-click order</button>
    <p id="status">Pending</p>
    
    <script>
        const menu = document.querySelector("#menu");
        
        menu.addEventListener("mouseenter", () => {
            document.querySelector("#panel").hidden = false;
        });
        
        document.querySelector("#order")
            .addEventListener("dblclick", () => {
                document.querySelector("#status")
                    .textContent = "Confirmed";
            });
    </script>
        
    """)

    page.get_by_role("button", name="Actions").hover()
    time.sleep(3)
    expect(
        page.get_by_text("Advanced options")
    ).to_be_visible()

    page.get_by_role("button", name="Double-click order").dblclick()
    time.sleep(3)
    expect(
        page.locator("#status")
    ).to_have_text("Confirmed")


def test_keyboard_interactions(page: Page):
    page.set_content("""
    <button id="save">Save</button>
    <p id="status">Unsaved</p>
    <p id="count">Save count: <input id="num" type="number" value="0"></p>
    
    <script>
        const saveButton = document.querySelector("#save");
        const status = document.querySelector("#status");
        const count = document.querySelector("#count");
        
        // Normal button behavior
        saveButton.addEventListener("click", () => {
        status.textContent = "Saved";
        });
        // Keyboard shortcut
        document.addEventListener("keydown", event => {
            if (
                (event.ctrlKey || event.metaKey) && 
                event.key.toLowerCase() === "s"
            ){
                event.preventDefault();
                
                // Trigger the existing Save button
                saveButton.click();
                const num = document.querySelector("#num");
                num.value = num.valueAsNumber + 1;
                }
        });    
    </script>
    """)
    status = page.locator("#status")
    expect(status).to_have_text("Unsaved")

    # simulate Ctrl+S on Windows/Linux,
    # or Cmd+S on macOS
    page.keyboard.press("ControlOrMeta+S")
    page.keyboard.press("ControlOrMeta+S")

    expect(status).to_have_text("Saved")
    expect(page.locator("#num")).to_have_value("2")

def test_shipping_dropdown(page: Page):
    page.set_content("""
        <label for="shipping">Shipping method</label>
        
        <select id="shipping">
            <option value="standard">Standard delivery</option>
            <option value="express">Express delivery</option>
            <option value="pickup">Store pickup</option>
        </select>
        
        <p id="result">Not shipped</p>
        
        <script>
            const shipping = document.querySelector("#shipping");
            
            shipping.addEventListener("change", event => {
                document.querySelector("#result")
                    .textContent = " Shipped: " + event.target.value;
            });
        </script>
    """)

    dropdown = page.get_by_label("Shipping method")

    dropdown.select_option(label="Store pickup")

    expect(dropdown).to_have_value("pickup")

    expect(
        page.locator("#result")
    ).to_have_text("Shipped: pickup")

def test_gift_wrapping_checkbox(page: Page):
    page.set_content("""
        <label>
            <input type="checkbox" id="gift">
            Add gift wrapping
        </label>
                     """)

    gift = page.get_by_role(
        "checkbox",
        name="Add gift wrapping"
    )

    # Verify initial state
    expect(gift).not_to_be_checked()

    # Enable gift wrapping
    gift.check()
    expect(gift).to_be_checked()

    # Checking again does not toggle it off
    gift.check()
    expect(gift).to_be_checked()

    # Disable gift wrapping
    gift.uncheck()
    expect(gift).not_to_be_checked()

    # Alternative API
    gift.set_checked(True)

    expect(gift).to_be_checked()

    

