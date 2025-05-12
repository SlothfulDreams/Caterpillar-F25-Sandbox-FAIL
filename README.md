# Sandbox F25 Caterpillar Challenge

Using old database info to build a new one for Cooper!

## Setup

### Required Packages

```bash
pip install requests pytest types-requests
```

or using the uv package manager

```bash
uv run
```
uv will auto install the required packages located in the .toml file
### Running the Main Application

```bash
python3 main.py
```

### Running Tests

```bash
python3 -m pytest
```

## Design Decisions

### Usage of Modules

I divided up each individual task group into their own
separate folders

**/api/** - The formatting logic of the data

**main.py** - Entry point of the function

**/tests/** - Tests for the functions

**/type_annotations/** - Type annotations to help with understanding what each input and output represents

This way it makes the code more readable and easier to maintain

### Functional Approach

I was debating whether to go with a function approach as opposed to a OOP approach and eventually settled for a function approach because of:

1. The task has a clear input and output data flow

2. The steps required do this data transformation has a very clear step (Create empty schema -> Add reviews -> sort -> calculate averages)

3. Easier to write tests as each function is isolated


### Type Annotations

I created a type annotation folder because it makes it easier for the reader to understand the kind of input and output a function will provide.

It also provides better error detection for the code within a IDE environment, makes its it easier to maintain

### Step-by-Step Data Processing

The data processing pipeline follows a clear, sequential approach:

1. Initialize the company structure with empty reviews
2. Add reviews to their respective roles 
3. Calculate statistics and sort reviews by rating

This stepwise approach makes the code easier to understand, debug, and maintain.

### Unit Test

I tested each function using the **Pytest** library as it is easier to use than the builtin **unittest** library

Unit Testing allows for a easier time and identify some edge cases

## Challenges Encountered

1. **Adding Reviews to the data**: Adding reviews to the data was the hardest part. To solve this issue I followed this step process.

Problem Statement: How can I identify which review belongs to which user, and which company?
- roleID -> Tells me the position/company (roleID are unique)
- ratingID -> Tells me which user made that review


    **Key observations**
    - The reviewId users do not actually matter in this format
    - We mainly just care about the name and the actual review
    - We can identify the location of where to insert a review by the id number of the job

    **Steps**
    1. Map userID to name (The only info we need from the users is their name, we do not need the list of reviews they made)

    2. From the list of reviews from the input data find where the review list is located for that roleId in our schema

    3. Insert the review into that position as we should have a reference to that location already from step ii

2. **Abstraction**: I noticed in a lot of my functions I had the repeated code of a double for loop transversal. To solve this issue I created my own higher order function called **role_data_cb** that takes in another function that relies on the data for the double for loop transversal. This makes my code easy to maintain if I was to implement more functions to the role data.

## Lessons Learned

1. **TypedDict vs. Regular Classes**: TypedDict is excellent for defining dictionary structures but has limitations with inheritance and runtime behavior. Understanding when to use type aliases versus custom classes was a valuable lesson.

2. **The Power of Good Test Fixtures**: Creating comprehensive test fixtures made writing tests much more straightforward and helped catch edge cases early.

3. **Function Signatures Matter**: Carefully designing function parameters and return types upfront saves significant refactoring later.

4. **Modularity Benefits**: Breaking down the solution into small, focused components made testing, debugging, and understanding the code much easier.

## Key Takeaways

- How to create my own custom type annotations for dictionaries

- I can create my own higher order functions for code abstraction rather then just relying on the standard map, filter, etc

- Learned what a confi file is for pytest

- Learned how to use uv python package manger and see the benefits it has compared to pip

## Future Improvements/Features to add if I were a member of Sandbox

If I had more time or if I was a member of Sandbox I would add:

**Add Data Validation**: Implement a way to detect outliers in data as some reviews could largely differ from the main consensus (This can flag for troll posts)

**Visualization Component**: Have a interface of all the data presented for a company rather then just straight up json data as its easier to view

**Export as different file types**: Feature to export to other file types such as excel, CSV, or like a PDF format

**Data Analytics**: Identify trends in the co-ops for example which is most popular, best quality of life, best pay, etc