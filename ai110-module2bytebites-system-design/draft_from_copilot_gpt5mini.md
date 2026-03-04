Generate a UML-style class diagram for these four classes. 

classDiagram
    class Customer {
        +String name
        +List~Order~ purchaseHistory
        +bool isVerified()
        +void addOrder(Order)
    }

    class MenuItem {
        +String name
        +float price
        +String category
        +int popularityRating
        +float getPrice()
    }

    class Menu {
        +List~MenuItem~ items
        +List~MenuItem~ filterByCategory(String)
        +void addItem(MenuItem)
        +void removeItem(MenuItem)
    }

    class Order {
        +List~MenuItem~ items
        +float total
        +void addItem(MenuItem)
        +void removeItem(MenuItem)
        +float computeTotal()
    }

    Customer "1" --> "0..*" Order : orders
    Menu o-- "0..*" MenuItem : contains
    Order "1" --> "*" MenuItem : items