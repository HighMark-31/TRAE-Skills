# Skill: gRPC Service Implementation

## Purpose
To build high-performance, low-latency inter-service communication using Protocol Buffers and HTTP/2.

## When to Use
- Microservices architectures.
- Internal APIs where low latency is critical.
- Polyglot environments (services in Go, Java, Python, Node).

## Procedure

### 1. Define Protocol Buffer (.proto)
Define the service contract and message structures.
```protobuf
syntax = "proto3";

package greeter;

service Greeter {
  rpc SayHello (HelloRequest) returns (HelloReply) {}
}

message HelloRequest {
  string name = 1;
}

message HelloReply {
  string message = 1;
}
```

### 2. Server Implementation (Node.js)
1.  **Load Proto**:
    ```javascript
    const grpc = require('@grpc/grpc-js');
    const protoLoader = require('@grpc/proto-loader');
    const packageDefinition = protoLoader.loadSync('greeter.proto');
    const greeterProto = grpc.loadPackageDefinition(packageDefinition).greeter;
    ```
2.  **Implement Logic**:
    ```javascript
    function sayHello(call, callback) {
      callback(null, { message: 'Hello ' + call.request.name });
    }
    ```
3.  **Start Server**:
    ```javascript
    const server = new grpc.Server();
    server.addService(greeterProto.Greeter.service, { sayHello: sayHello });
    server.bindAsync('0.0.0.0:50051', grpc.ServerCredentials.createInsecure(), () => {
      server.start();
    });
    ```

### 3. Client Implementation
```javascript
const client = new greeterProto.Greeter('localhost:50051', grpc.credentials.createInsecure());

client.sayHello({ name: 'World' }, (err, response) => {
  console.log('Greeting:', response.message);
});
```

## Constraints
- **Browser Support**: Browsers do not support gRPC natively. Use gRPC-Web proxy if frontend access is needed.
- **Debugging**: Binary format is not human-readable. Use tools like BloomRPC or Postman (gRPC support) for testing.

## Expected Output
Strongly-typed, efficient communication channel between services, significantly faster than JSON/REST.
