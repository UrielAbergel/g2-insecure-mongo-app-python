print("MongoDB init script is running...");

// 1. Root user is created automatically by MONGO_INITDB_ROOT_USERNAME/PASSWORD env vars.
// No need to create it manually in this script.
const adminDb = db.getSiblingDB('admin');

// 2. Switch to application DB
const appDb = db.getSiblingDB('mydb');

// 3. Create collections if not exist
const collections = appDb.getCollectionNames();

if (!collections.includes('items')) {
  print("Creating 'items' collection...");
  appDb.createCollection('items');
} else {
  print("'items' collection already exists.");
}

if (!collections.includes('users')) {
  print("Creating 'users' collection...");
  appDb.createCollection('users');
} else {
  print("'users' collection already exists.");
}

// 4. Insert users only if they don't exist
// Passwords are hashed with PBKDF2-SHA256 (100k iterations), format: salt_hex:dk_hex
const users = [
  { username: "admin", credentialHash: "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6:b7f6d8e141539871cf5f6f9bec09cbe5ac9dc4b1d4570d84113e8986303627f4", role: "admin" },
  { username: "reader", credentialHash: "b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6:22e4e57b306c162244344415915bdc89253ac639fec43b9b5363deb856ddfd3a", role: "reader" },
  { username: "writer", credentialHash: "c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6:a4abb94c1fa2e3d55274ec50957b94e15d41d3aebfb1420b3a21e7e596eba083", role: "writer" }
];

users.forEach(user => {
  if (!appDb.users.findOne({ username: user.username })) {
    print(`Inserting user '${user.username}'...`);
    appDb.users.insertOne(user);
  } else {
    print(`User '${user.username}' already exists.`);
  }
});
