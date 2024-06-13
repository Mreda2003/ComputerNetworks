# Online Store

## Overview
This project is a simple socket-based application for managing an online store's order system. The server handles client connections, processes their orders, and updates the inventory in real-time. Multiple clients can connect to the server concurrently, thanks to multithreading, ensuring a responsive experience.

## Technologies Used
- **Python**: The core programming language used for implementing the project.
- **Socket Programming**: Used to handle client-server communication over TCP.
- **Threading**: Utilized to manage multiple clients simultaneously, allowing the server to handle concurrent requests.
- **Synchronization (Lock)**: Employed to manage access to shared resources (inventory data) and prevent race conditions.

## Aims
1. **Client Management**: Efficiently handle multiple clients, each interacting with the server to browse products, place orders, and receive confirmations.
2. **Order Processing**: Allow clients to view available products, select quantities, and place orders, ensuring the inventory is updated in real-time.
3. **Concurrency Handling**: Utilize threading to serve multiple clients simultaneously without performance degradation.
4. **Data Integrity**: Implement synchronization mechanisms to ensure the inventory data remains consistent even with concurrent access.

## Detailed Functionality

### Initialization
- The server binds to a specified IP (`127.0.0.1`) and port (`9000`).
- A list of products, their quantities, and prices are initialized.

### Client Interaction
1. **Client Connection**:
   - The server listens for incoming client connections.
   - Each client is handled in a separate thread to allow concurrent interactions.
   
2. **Client Details Collection**:
   - The server prompts the client to provide their name and address.

3. **Product Display**:
   - The client is greeted and asked if they wish to place an order.
   - Available products, their prices, and quantities are displayed to the client.

4. **Order Placement**:
   - The client selects products and specifies the desired quantities.
   - The server checks if the requested quantity is available and prompts the client to add more items or finalize the order.

5. **Order Confirmation**:
   - The server displays the client's order summary and total bill.
   - The client confirms if they wish to proceed with the checkout.

6. **Inventory Update**:
   - With a synchronization lock, the server checks if the products are still available in the requested quantities.
   - If available, the inventory is updated, and the client is informed of the successful order.
   - If not, the client is notified that another client has purchased the items, and the order cannot be fulfilled.

### Exception Handling and Cleanup
- Any issues encountered during the client interaction result in a polite error message being sent to the client.
- The client session is closed after the interaction, and the thread managing the client is terminated.

## Running the Server
1. Ensure you have Python installed on your machine.
2. Save the server code in a file, for example, `server.py`.
3. Run the server using the command:
    ```sh
    python server.py
    ```
4. The server will start listening for client connections on `127.0.0.1:9000`.