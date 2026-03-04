classDiagram
    class Customer {
        -String name
        -List~Order~ purchaseHistory
        +isVerified() bool
    }

    class MenuItem {
        -String name
        -float price
        -String category
        -int popularityRating
    }

    class Menu {
        -List~MenuItem~ items
        +filterByCategory(String category) List~MenuItem~
    }

    class Order {
        -List~MenuItem~ items
        +getTotal() float
    }

    Customer "1" --> "*" Order : places
    Order "1" --> "1..*" MenuItem : contains
    Menu "1" --> "*" MenuItem : holds
