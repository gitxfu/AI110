This is generated using .github/agents/bytebites_design_agent.md

classDiagram
    class Customer {
        - name: String
        - purchaseHistory: List~Order~
        + verify(): Boolean
        + addOrder(order: Order): void
        + getPurchaseHistory(): List~Order~
    }

    class MenuItem {
        - name: String
        - price: Float
        - category: String
        - popularityRating: Int
        + getPrice(): Float
    }

    class Menu {
        - items: List~MenuItem~
        + addItem(item: MenuItem): void
        + removeItem(item: MenuItem): void
        + filterByCategory(category: String): List~MenuItem~
        + listAll(): List~MenuItem~
    }

    class Order {
        - items: List~MenuItem~
        - customer: Customer
        + addItem(item: MenuItem): void
        + removeItem(item: MenuItem): void
        + total(): Float
    }

    Menu "1" o-- "*" MenuItem : contains
    Order "1" o-- "*" MenuItem : includes
    Order --> "1" Customer : belongsTo
    Customer "1" o-- "*" Order : orders