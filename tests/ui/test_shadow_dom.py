from playwright.sync_api import Page, expect


def test_payment_shadow_dom(page: Page):
    page.set_content("""
    <h1>Checkout</h1>
    <payment-widget></payment-widget>
    
    <p id="result">Pending</p>
    
    <script>
        class PaymentWidget extends HTMLElement {
            connectedCallback() {
            const shadow = this.attachShadow({
            mode: "open"
            });
            
            shadow.innerHTML = `
            <label for="card">Card number</label>
            <input id="card" type="text">
            <label for="date">Expiration date</label>
            <input id="date" type="text">
            
            
            <button type="button">Pay</button>
            `;
            
            shadow.querySelector("button")
                .addEventListener("click", () => {
                const number = 
                    shadow.querySelector("#card").value;
                const date = 
                    shadow.querySelector("#date").value;
                document.querySelector("#result")
                    .textContent = "Paid: " + number  + ";" + "Expiration date: " + date;
                
                }
                );
            }
        }
        
        customElements.define(
        "payment-widget",
        PaymentWidget,
        );
    </script>
    """)

    # Locate input inside Shadow DOM
    card_input = page.get_by_role("textbox", name="Card number")

    expiration_date = page.get_by_role("textbox", name="Expiration date")

    expiration_date.fill("Jun 31")

    card_input.fill("TEST-1234")

    expect(card_input).to_have_value("TEST-1234")

    # Locate button inside Shadow DOM
    page.get_by_role("button", name="Pay").click()

    # Verify result outside Shadow DOM
    expect(
        page.locator("#result")
    ).to_have_text("Paid: TEST-1234;Expiration date: Jun 31")