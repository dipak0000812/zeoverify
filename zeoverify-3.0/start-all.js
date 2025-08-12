const { spawn } = require('child_process');
const path = require('path');

console.log('🚀 Starting Zeoverify Services...\n');

// Function to start a service
function startService(name, command, args, cwd) {
  console.log(`📡 Starting ${name}...`);
  
  const child = spawn(command, args, {
    cwd: path.join(__dirname, cwd),
    stdio: 'pipe',
    shell: true
  });

  child.stdout.on('data', (data) => {
    console.log(`[${name}] ${data.toString().trim()}`);
  });

  child.stderr.on('data', (data) => {
    console.error(`[${name} ERROR] ${data.toString().trim()}`);
  });

  child.on('close', (code) => {
    console.log(`[${name}] Process exited with code ${code}`);
  });

  return child;
}

// Start services
const services = [
  {
    name: 'AI Engine',
    command: 'python',
    args: ['app.py'],
    cwd: 'ai-engine'
  },
  {
    name: 'Backend',
    command: 'npm',
    args: ['start'],
    cwd: 'backend'
  },
  {
    name: 'Frontend',
    command: 'npm',
    args: ['run', 'dev'],
    cwd: 'frontend'
  }
];

// Start all services
services.forEach(service => {
  startService(service.name, service.command, service.args, service.cwd);
});

console.log('\n✅ All services started!');
console.log('🌐 Frontend: http://localhost:5173');
console.log('🔧 Backend: http://localhost:5000');
console.log('🧠 AI Engine: http://localhost:5001');
console.log('⛓️  Blockchain: http://localhost:8545');
console.log('\nPress Ctrl+C to stop all services'); 