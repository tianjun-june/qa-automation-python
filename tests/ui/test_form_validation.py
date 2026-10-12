from playwright.sync_api import Page, expect


def test_order_form_validation(page: Page):
    page.set_content("""
        <form id="order-form">
            <label for="email">Email</label>
            <input 
                id="email"
                type="email"
                required
            >
            
            <label for="quantity">Quantity</label>
            <input 
                id="quantity"
                type="number"
                min="1"
                max="10"
                required"
            >
            
            <label for="reference">Order reference</label>
            <input 
                id="reference"
                value="ORDER-123"
                readonly
            >
            
            <label for="promotion">Promotion code</label>
            <input 
                id="promotion"
                disabled
            >
            
            <button type="submit">Place order</button>
            </form>
            
            <p id="status">Not submitted</p>
            
            <script>
                const form = document.querySelector("#order-form");
                
                form.addEventListener("submit", event => {
                    event.preventDefault();
                    
                    document.querySelector("#status")
                        .textContent = "Order submitted";
                });
            </script>
    """)

    email = page.get_by_role("textbox", name="Email")
    quantity = page.get_by_role("spinbutton", name="Quantity")
    reference = page.get_by_role("textbox", name="Order reference")

    promotion = page.get_by_role("textbox", name="Promotion code")
    submit = page.get_by_role("button", name="Place order")
    status = page.locator("#status")

    #1. Verify element properties
    expect(email).to_have_attribute("required", "")
    expect(email).to_be_editable()

    expect(reference).not_to_be_editable()
    expect(reference).to_have_value("ORDER-123")

    expect(promotion).to_be_disabled()

    # 2.Submit with empty required fields
    submit.click()

    expect(email).to_match_aria_snapshot("- textbox \"Email\"")
    expect(page.locator("#email:invalid")).to_be_visible()
    expect(status).to_have_text("Not submitted")
    # page.pause()

    # 3.Enter invalid email
    email.fill("invalid-email")
    expect(page.locator("#email:invalid")).to_be_visible()

    #4. Enter valid email but invalid quantity
    email.fill("qa@example.com")
    quantity.fill("0")

    expect(page.locator("#email:valid")).to_be_visible()
    expect(page.locator("#quantity:invalid")).to_be_visible()

    # 5. Complete valid form data
    quantity.fill("2")

    expect(page.locator("#quantity:valid")).to_be_visible()

    submit.click()

    expect(status).to_have_text("Order submitted")