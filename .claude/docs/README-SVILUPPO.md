# Sviluppo Software - Best Practices e Guidelines

## Indice
1. [Principi Generali](#principi-generali)
2. [Angular Best Practices](#angular-best-practices)
3. [Spring Boot Best Practices](#spring-boot-best-practices)
4. [Python Best Practices](#python-best-practices)
5. [Architettura Software](#architettura-software)
6. [Testing](#testing)
7. [DevOps e CI/CD](#devops-e-cicd)
8. [Code Quality](#code-quality)

---

## Principi Generali

### SOLID Principles
- **S**ingle Responsibility: Una classe, una responsabilità
- **O**pen/Closed: Aperta per estensione, chiusa per modifica
- **L**iskov Substitution: Le sottoclassi devono essere sostituibili alle classi base
- **I**nterface Segregation: Interfacce specifiche meglio di una generale
- **D**ependency Inversion: Dipendere da abstractions, non da concretions

### Clean Code Principles
- Nomi significativi e pronunciabili
- Funzioni piccole (max 20 righe ideale)
- Un livello di astrazione per funzione
- DRY (Don't Repeat Yourself)
- KISS (Keep It Simple, Stupid)
- YAGNI (You Aren't Gonna Need It)

### Design Patterns Comuni
- **Creazionali**: Singleton, Factory, Builder
- **Strutturali**: Adapter, Decorator, Facade
- **Comportamentali**: Observer, Strategy, Command

---

## Angular Best Practices

### Struttura Progetto
```
src/
├── app/
│   ├── core/                 # Singleton services, guards
│   │   ├── services/
│   │   ├── guards/
│   │   ├── interceptors/
│   │   └── core.module.ts
│   ├── shared/               # Componenti, pipes, directives riusabili
│   │   ├── components/
│   │   ├── pipes/
│   │   ├── directives/
│   │   └── shared.module.ts
│   ├── features/             # Feature modules
│   │   ├── auth/
│   │   ├── dashboard/
│   │   └── ...
│   └── app.module.ts
├── assets/
└── environments/
```

### Component Guidelines
- Un componente per file
- OnPush change detection quando possibile
- Unsubscribe da Observables (async pipe o takeUntil)
- Smart vs Dumb components
  - **Smart**: Gestione stato, business logic
  - **Dumb**: Solo presentazione, input/output

```typescript
// Esempio Dumb Component
@Component({
  selector: 'app-user-card',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class UserCardComponent {
  @Input() user: User;
  @Output() userClick = new EventEmitter<User>();
}

// Unsubscribe pattern
private destroy$ = new Subject<void>();

ngOnInit() {
  this.service.getData()
    .pipe(takeUntil(this.destroy$))
    .subscribe(data => {});
}

ngOnDestroy() {
  this.destroy$.next();
  this.destroy$.complete();
}
```

### Services
- Providere in root quando singleton
- Dependency Injection correttamente
- Gestione errori centralizzata

```typescript
@Injectable({ providedIn: 'root' })
export class DataService {
  constructor(private http: HttpClient) {}

  getData(): Observable<Data> {
    return this.http.get<Data>('/api/data')
      .pipe(
        catchError(this.handleError),
        retry(2)
      );
  }
}
```

### Performance
- Lazy loading dei moduli
- TrackBy nelle *ngFor
- Virtual scrolling per liste lunghe
- Preloading strategies
- Bundle size optimization (analizzare con webpack-bundle-analyzer)

---

## Spring Boot Best Practices

### Struttura Progetto
```
src/main/java/com/example/project/
├── config/              # Configurazioni
├── controller/          # REST controllers
├── service/             # Business logic
├── repository/          # Data access
├── model/
│   ├── entity/         # JPA entities
│   └── dto/            # Data Transfer Objects
├── exception/          # Custom exceptions
├── security/           # Security config
└── util/               # Utilities
```

### Controller Layer
```java
@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @GetMapping("/{id}")
    public ResponseEntity<UserDTO> getUser(@PathVariable Long id) {
        return ResponseEntity.ok(userService.getUser(id));
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public UserDTO createUser(@Valid @RequestBody CreateUserDTO dto) {
        return userService.createUser(dto);
    }
}
```

### Service Layer
```java
@Service
@Transactional
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;
    private final UserMapper userMapper;

    @Transactional(readOnly = true)
    public UserDTO getUser(Long id) {
        User user = userRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("User not found"));
        return userMapper.toDTO(user);
    }
}
```

### Best Practices
- Usare DTOs per API (non esporre entities)
- Validation con Bean Validation (@Valid, @NotNull, etc.)
- Exception handling centralizzato con @ControllerAdvice
- Lombok per ridurre boilerplate
- MapStruct per mapping entity-dto
- Profiles per ambienti diversi (dev, test, prod)

### Database
- Flyway/Liquibase per migrations
- Connection pooling (HikariCP)
- Lazy loading attento (N+1 queries)
- Indici database appropriati
- Query optimization (@Query, Specifications)

### Security
```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) {
        return http
            .csrf().disable()
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/public/**").permitAll()
                .anyRequest().authenticated()
            )
            .oauth2ResourceServer(OAuth2ResourceServerConfigurer::jwt)
            .build();
    }
}
```

---

## Python Best Practices

### Struttura Progetto
```
project/
├── src/
│   └── package/
│       ├── __init__.py
│       ├── module1.py
│       └── module2.py
├── tests/
├── docs/
├── requirements.txt
├── setup.py
└── README.md
```

### Code Style
- PEP 8 compliance
- Type hints (Python 3.5+)
- Docstrings (Google style o NumPy style)

```python
from typing import List, Optional

def process_data(
    items: List[str],
    filter_empty: bool = True
) -> List[str]:
    """
    Process a list of items.

    Args:
        items: List of strings to process
        filter_empty: Whether to remove empty strings

    Returns:
        Processed list of strings

    Raises:
        ValueError: If items is empty
    """
    if not items:
        raise ValueError("Items list cannot be empty")

    result = [item.strip() for item in items]

    if filter_empty:
        result = [item for item in result if item]

    return result
```

### Virtual Environments
```bash
# Creare env
python -m venv venv

# Attivare
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Requirements
pip freeze > requirements.txt
pip install -r requirements.txt
```

### Best Practices
- Context managers (with statement)
- List comprehensions (leggibili)
- Generators per grandi dataset
- Exception handling specifico
- Logging invece di print

```python
# Context manager
with open('file.txt', 'r') as f:
    data = f.read()

# List comprehension
squares = [x**2 for x in range(10) if x % 2 == 0]

# Generator
def read_large_file(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            yield line.strip()

# Logging
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Process started")
```

---

## Architettura Software

### Layered Architecture
```
Presentation Layer (UI/API)
    ↓
Business Logic Layer (Services)
    ↓
Data Access Layer (Repositories)
    ↓
Database
```

### Microservices Considerations
- Single Responsibility per servizio
- API Gateway per routing
- Service discovery
- Distributed tracing
- Circuit breakers (resilienza)
- Event-driven communication

### Clean Architecture
- Entities (core business logic)
- Use Cases (application business rules)
- Interface Adapters (controllers, presenters)
- Frameworks & Drivers (external agencies)

Dependency Rule: Dipendenze verso l'interno

---

## Testing

### Testing Pyramid
```
        /\
       /UI\         (few)
      /----\
     / API  \       (some)
    /--------\
   /   Unit   \     (many)
  /------------\
```

### Unit Testing

#### Angular (Jasmine/Karma)
```typescript
describe('UserService', () => {
  let service: UserService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [UserService]
    });
    service = TestBed.inject(UserService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  it('should fetch users', () => {
    const mockUsers = [{id: 1, name: 'Test'}];

    service.getUsers().subscribe(users => {
      expect(users).toEqual(mockUsers);
    });

    const req = httpMock.expectOne('/api/users');
    expect(req.request.method).toBe('GET');
    req.flush(mockUsers);
  });
});
```

#### Spring Boot (JUnit 5 + Mockito)
```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository repository;

    @InjectMocks
    private UserService service;

    @Test
    void shouldGetUser() {
        User user = new User(1L, "Test");
        when(repository.findById(1L))
            .thenReturn(Optional.of(user));

        UserDTO result = service.getUser(1L);

        assertNotNull(result);
        assertEquals("Test", result.getName());
        verify(repository).findById(1L);
    }
}
```

#### Python (pytest)
```python
import pytest

def test_process_data():
    items = ["  hello  ", "world"]
    result = process_data(items)

    assert result == ["hello", "world"]
    assert len(result) == 2

def test_process_data_empty_raises():
    with pytest.raises(ValueError):
        process_data([])
```

### Integration Testing
- Test API endpoints end-to-end
- Test con database (testcontainers)
- Mocking di servizi esterni

### E2E Testing
- Cypress (Angular)
- Selenium
- Playwright

---

## DevOps e CI/CD

### Version Control (Git)
```bash
# Branch strategy: GitFlow
main          # Production
develop       # Development
feature/*     # Features
hotfix/*      # Urgent fixes
release/*     # Release preparation

# Conventional Commits
feat: add user login
fix: resolve null pointer in service
docs: update API documentation
refactor: simplify user validation
test: add unit tests for auth
```

### CI/CD Pipeline
```yaml
# Esempio GitHub Actions
name: CI/CD

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Node
        uses: actions/setup-node@v2
      - name: Install dependencies
        run: npm ci
      - name: Run tests
        run: npm test
      - name: Build
        run: npm run build

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: ./deploy.sh
```

### Docker
```dockerfile
# Multi-stage build
FROM node:18 AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
```

---

## Code Quality

### Tools
- **Linting**: ESLint (JS/TS), Checkstyle (Java), Pylint (Python)
- **Formatting**: Prettier, Black (Python)
- **Static Analysis**: SonarQube
- **Code Coverage**: Istanbul (JS), JaCoCo (Java), Coverage.py

### Code Review Checklist
- [ ] Code segue gli standard del progetto
- [ ] Test adeguati presenti
- [ ] Nomi variabili/funzioni chiari
- [ ] Nessun codice commentato
- [ ] Gestione errori appropriata
- [ ] Performance considerata
- [ ] Security vulnerabilities controllate
- [ ] Documentazione aggiornata

### Metrics da Monitorare
- Code coverage (target: >80%)
- Cyclomatic complexity (basso)
- Code duplication (< 3%)
- Technical debt ratio
- Bug density

---

**Ultimo aggiornamento:** 2026-01-03

**Note:** Best practices evolvono. Rimanere aggiornati su nuove versioni framework e patterns emergenti.
