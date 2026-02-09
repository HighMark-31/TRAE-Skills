# Skill: Offline-First Mobile Architecture

## Purpose
To design mobile apps that remain fully functional without an internet connection, syncing data when connectivity is restored.

## When to Use
- Field service apps (inspections, delivery).
- Apps used in areas with poor connectivity.
- To improve perceived performance (optimistic UI).

## Procedure

### 1. Local Database Selection
- **WatermelonDB**: High performance, built on SQLite, reactive. Great for complex relational data.
- **Expo SQLite**: Low-level access to SQLite.
- **Realm**: Object-oriented, fast.
- **TanStack Query (React Query)**: Good for caching API responses, but not a full DB.

### 2. Architecture Pattern (Sync Engine)
1.  **Read**: Always read from Local DB for UI.
2.  **Write**:
    - Write to Local DB immediately.
    - Mark record as `dirty` or `pending_sync`.
    - Trigger background sync.
3.  **Sync Process**:
    - **Push**: Send pending local changes to Backend.
    - **Pull**: Fetch new changes from Backend (using `last_synced_at` timestamp).
    - **Resolve Conflicts**: Last-write-wins or user intervention.

### 3. Network State Management
Use `expo-network` or `@react-native-community/netinfo`.
```tsx
const netInfo = useNetInfo();
useEffect(() => {
  if (netInfo.isConnected) {
    syncData();
  }
}, [netInfo.isConnected]);
```

### 4. Implementation Example (WatermelonDB)
Define Schema -> Define Models -> Write Sync Logic using `synchronize()` helper provided by WatermelonDB, which handles the "Push/Pull" logic.

## Constraints
- **Storage Limits**: Mobile devices have limited storage; clean up old data periodically.
- **Conflict Resolution**: Hardest part. Keep logic simple (server authority) if possible.
- **Security**: Encrypt sensitive local data (e.g., using SQLCipher).

## Expected Output
An app that loads content instantly offline and synchronizes data invisibly in the background.
