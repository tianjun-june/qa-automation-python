import pytest
from playwright.sync_api import Page, expect


FORM_HTML =  """
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
                required
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
    """

def test_order_form_validation(page: Page):
    page.set_content(FORM_HTML)

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

    assert email.evaluate("(element) => element.validity.valueMissing")
    # page.pause()

    # 3.Enter invalid email
    email.fill("invalid-email")
    expect(page.locator("#email:invalid")).to_be_visible()

    assert email.evaluate("(element) => element.validity.typeMismatch")
    print(email.evaluate("(element) => element.validationMessage"))

    #4. Enter valid email but invalid quantity
    email.fill("qa@example.com")
    quantity.fill("0")

    expect(page.locator("#email:valid")).to_be_visible()
    expect(page.locator("#quantity:invalid")).to_be_visible()
    assert quantity.evaluate("(element) => element.validity.rangeUnderflow")

    # 5. Complete valid form data
    quantity.fill("2")

    expect(page.locator("#quantity:valid")).to_be_visible()

    submit.click()

    expect(status).to_have_text("Order submitted")

@pytest.mark.parametrize(
    "email_value, quantity_value, invalid_field, reason",
    [
        pytest.param(
            "", "2", "email", "valueMissing",
            id="email-required"
        ),
        pytest.param(
            "qw", "2", "email", "typeMismatch",
            id="invalid-email"
        ),
        pytest.param(
            "qw@", "2", "email", "typeMismatch",
            id="invalid-email-containing@"
        ),
        pytest.param(
            "qa@example.com", "", "quantity", "valueMissing",
            id="quantity-required"
        ),
        pytest.param(
            "qa@example.com", "0", "quantity", "rangeUnderflow",
            id="quantity-below-min"
        ),
        pytest.param(
            "qa@example.com", "11", "quantity", "rangeOverflow",
            id="quantity-above-max"
        ),
    ]
)
def test_order_form_validation_param(page: Page, email_value, quantity_value, invalid_field, reason):
    page.set_content(FORM_HTML)

    page.get_by_label("Email").fill(email_value)
    page.get_by_label("Quantity").fill(quantity_value)

    page.get_by_role(
        "button", name="Place order"
    ).click()

    # Identity the invalid field
    field = page.locator(f"#{invalid_field}")

    # verify browser-native invalid state
    print(f"field required: {field.get_attribute("required")}")
    print(f"invalid field: {invalid_field}")
    expect(field).to_have_attribute("required", "")


    expect(
        page.locator(f"#{invalid_field}:invalid")
    ).to_be_visible()

    # Verify the precise validation reason
    actual_reason = field.evaluate(
        "(el, reason) => el.validity[reason]", reason)

    assert actual_reason is True

    #verify invalid data was not submitted
    expect(
        page.locator("#status")
    ).to_have_text("Not submitted")

@pytest.mark.parametrize(
    "quantity",
    [
        pytest.param("1", id="minimum"),
        pytest.param("10", id="maximum"),
    ],
)
def test_valid_order_boundaries(
        page: Page,
        quantity,
):
    page.set_content(FORM_HTML)

    email = page.get_by_label("Email")
    quantity_field = page.get_by_label("Quantity")

    email.fill("qa@example.com")
    quantity_field.fill(quantity)

    #Both fields should be valid
    expect(page.locator("#email:valid")).to_be_visible()
    expect(page.locator("#quantity:valid")).to_be_visible()

    page.get_by_role(
        "button", name="Place order"
    ).click()

    expect(
        page.locator("#status")
    ).to_have_text("Order submitted")