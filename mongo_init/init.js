print("📢 MongoDB init script is running...");

// 1. Create root user only if it doesn't exist
const adminDb = db.getSiblingDB('admin');

if (!adminDb.getUser("root")) {
  print("✅ Creating root user...");
  adminDb.createUser({
    user: "root",
    pwd: "example",
    roles: [{ role: "root", db: "admin" }]
  });
} else {
  print("ℹ️ Root user already exists.");
}

// 2. Switch to application DB
const appDb = db.getSiblingDB('mydb');

// 3. Create collections if not exist
const collections = appDb.getCollectionNames();

if (!collections.includes('items')) {
  print("✅ Creating 'items' collection...");
  appDb.createCollection('items');
} else {
  print("ℹ️ 'items' collection already exists.");
}

if (!collections.includes('users')) {
  print("✅ Creating 'users' collection...");
  appDb.createCollection('users');
} else {
  print("ℹ️ 'users' collection already exists.");
}

// 4. Insert users only if they don't exist
const users = [
  { username: "admin", passwordHash: "d033e22ae348aeb5660fc2140aec35850c4da997", role: "admin" },
  { username: "reader", passwordHash: "24b55fe81e9e7b11798d3a4e4677dd48ffc81559", role: "reader" },
  { username: "writer", passwordHash: "fe28f10d2c6dab4e315f2659adaa6a4f16b5e4b8", role: "writer" }
];

users.forEach(user => {
  if (!appDb.users.findOne({ username: user.username })) {
    print(`✅ Inserting user '${user.username}'...`);
    appDb.users.insertOne(user);
  } else {
    print(`ℹ️ User '${user.username}' already exists.`);
  }
});
