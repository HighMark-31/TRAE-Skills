# Skill: WebSocket Implementation (Socket.io)

## Purpose
To enable real-time, bi-directional event-based communication between the client and server.

## When to Use
- Chat applications.
- Live notifications/alerts.
- Real-time dashboards or collaborative editing.

## Procedure
1.  **Initialize Server**: Attach Socket.io to the HTTP server instance.
2.  **Handle Connection**: Listen for `connection` events.
3.  **Authentication**: Validate the handshake (e.g., verify JWT in query params or headers) before allowing connection.
4.  **Define Events**:
    - `emit` to send data to client(s).
    - `on` to listen for data from client.
5.  **Rooms/Namespaces**: Use rooms to group sockets (e.g., `socket.join('room_123')`) for targeted broadcasting.
6.  **Handle Disconnect**: Clean up resources when a user leaves.

## Constraints
- WebSockets are stateful; scaling requires a Redis adapter to sync events across multiple server instances.
- Handle reconnection logic on the client side.
- Be mindful of open connection limits.

## Expected Output
A WebSocket server module handling connection, auth, and event routing for real-time features.
