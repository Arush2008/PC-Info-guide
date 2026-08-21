(() => {
    const modal = document.getElementById("detailsModal");
    if (!modal) return;

    const modalBox = modal.querySelector(".modal_box");
    modalBox.innerHTML = `
        <button type="button" class="modal_close" aria-label="Close component details">&times;</button>
        <div class="component_modal_layout">
            <div class="modal_image_panel"><img class="modal_image" alt=""></div>
            <div class="modal_content">
                <p class="modal_eyebrow">Component details</p>
                <p class="modal_brand"></p>
                <h1 class="modal_title"></h1>
                <dl class="modal_details"></dl>
                <div class="modal_footer">
                    <button type="button" class="modal_add_button">Add to PC Builder</button>
                    <span class="modal_price"></span>
                </div>
            </div>
        </div>`;

    const closeButton = modal.querySelector(".modal_close");
    const imagePanel = modal.querySelector(".modal_image_panel");
    const image = modal.querySelector(".modal_image");
    const brand = modal.querySelector(".modal_brand");
    const title = modal.querySelector(".modal_title");
    const details = modal.querySelector(".modal_details");
    const price = modal.querySelector(".modal_price");
    const addButton = modal.querySelector(".modal_add_button");
    let activeComponent = null;

    const formatPrice = (amount) => new Intl.NumberFormat("en-NZ", {
        style: "currency", currency: "NZD", maximumFractionDigits: 2
    }).format(amount);

    const closeModal = () => {
        modal.classList.remove("open");
        document.body.classList.remove("modal_open");
    };

    const showDetails = async (card) => {
        const type = card.dataset.componentType;
        const id = card.dataset.componentId;
        if (!type || !id) return;

        modal.classList.add("open");
        document.body.classList.add("modal_open");
        brand.textContent = "Loading component…";
        title.textContent = "";
        details.innerHTML = "";
        price.textContent = "";
        imagePanel.hidden = true;
        addButton.disabled = true;

        const response = await fetch(`/api/components/${encodeURIComponent(type)}/${encodeURIComponent(id)}`);
        if (!response.ok) {
            brand.textContent = "Unable to load this component.";
            return;
        }

        const component = await response.json();
        activeComponent = component;
        brand.textContent = component.brand;
        title.textContent = component.model;
        price.textContent = formatPrice(component.price);
        imagePanel.hidden = !component.image_url;
        if (component.image_url) {
            image.src = component.image_url;
            image.alt = `${component.brand} ${component.model}`;
        }

        details.innerHTML = component.details.map((detail) =>
            `<div><dt>${detail.label}</dt><dd>${detail.value}</dd></div>`
        ).join("");
        addButton.disabled = false;
        addButton.textContent = "Add to PC Builder";
    };

    document.querySelectorAll(".component_card[data-component-type][data-component-id]").forEach((card) => {
        card.addEventListener("click", () => showDetails(card));
    });

    addButton.addEventListener("click", async () => {
        if (!activeComponent) return;
        addButton.disabled = true;
        addButton.textContent = "Adding…";
        const response = await fetch(`/api/builder/selection/${encodeURIComponent(activeComponent.component_type)}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id: activeComponent.component_id })
        });
        const result = await response.json();
        if (!response.ok) {
            addButton.textContent = result.error || "Try again";
            addButton.disabled = false;
            return;
        }
        addButton.textContent = "Added to Builder ✓";
    });

    closeButton.addEventListener("click", closeModal);
    modal.addEventListener("click", (event) => { if (event.target === modal) closeModal(); });
    document.addEventListener("keydown", (event) => { if (event.key === "Escape") closeModal(); });
})();
