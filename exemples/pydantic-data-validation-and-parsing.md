# Pydantic — Validação e Parsing de Dados

[Pydantic](https://docs.pydantic.dev/) é a biblioteca de validação de dados mais popular do ecossistema Python.  
Ela usa **anotações de tipo** para declarar o formato esperado dos dados — e valida, converte e rejeita entradas automaticamente.

Tópicos cobertos neste notebook:

| Seção | O que cobre |
|-------|-------------|
| `BaseModel` | definição declarativa de modelos e parsing de dicionários |
| `Field` | restrições numéricas, de lista e decimais |
| `field_validator` / `model_validator` | lógica de validação customizada por campo ou por modelo |
| `computed_field` / `default_factory` | campos derivados e valores padrão dinâmicos |
| `alias` / `TypeAdapter` | interoperabilidade com APIs externas |


```python
import datetime
import uuid
from dataclasses import Field

from pydantic import BaseModel, PositiveInt, EmailStr, field_validator, UUID4
from pydantic_core.core_schema import computed_field


class Author(BaseModel):
    name: str
    age: PositiveInt
    email: EmailStr | None = None

class Book(BaseModel):
    title: str
    pages: PositiveInt
    authors: list[Author]

hobbit = Book.model_validate({
    "title": "The Hobbit",
    "pages": 300,
    "authors": [{"name": "J.R.R.", "age": 32, "email": None}]
})


print(hobbit)
# Generate a dictionary representation of the model
# {instance}.model_dump() -> dict
print(hobbit.model_dump())

```

    title='The Hobbit' pages=300 authors=[Author(name='J.R.R.', age=32, email=None)]
    {'title': 'The Hobbit', 'pages': 300, 'authors': [{'name': 'J.R.R.', 'age': 32, 'email': None}]}


## `BaseModel` — definição declarativa de modelos

Um modelo Pydantic é uma classe que herda de `BaseModel`. Cada atributo com anotação de tipo define um campo validado.

- `PositiveInt` garante `> 0` sem nenhum código extra.  
- `EmailStr` valida o formato de e-mail automaticamente.  
- `model_validate(dict)` constrói o modelo a partir de um dicionário bruto.  
- `model_dump()` serializa a instância de volta para `dict`.

> Modelos podem ser **aninhados**: `Book.authors` é `list[Author]` — o Pydantic valida cada item recursivamente.


```python
%xmode
hobbit = Book.model_validate({
    "title": "The Hobbit",
    "pages": 300,
    "authors": [{"name": "J.R.R.", "age": -32, "email": None}]
})
```

    Exception reporting mode: Verbose



    ---------------------------------------------------------------------------

    ValidationError                           Traceback (most recent call last)

    Cell In[11], line 2
          1 get_ipython().run_line_magic('xmode', '')
    ----> 2 hobbit = Book.model_validate({
          3     "title": "The Hobbit",
          4     "pages": 300,
          5     "authors": [{"name": "J.R.R.", "age": -32, "email": None}]


    File ~/dev/victor-broering/.venv/lib/python3.14/site-packages/pydantic/main.py:732, in BaseModel.model_validate(cls=<class '__main__.Book'>, obj={'authors': [{'age': -32, 'email': None, 'name': 'J.R.R.'}], 'pages': 300, 'title': 'The Hobbit'}, strict=None, extra=None, from_attributes=None, context=None, by_alias=None, by_name=None)
        726 if by_alias is False and by_name is not True:
        727     raise PydanticUserError(
        728         'At least one of `by_alias` or `by_name` must be set to True.',
        729         code='validate-by-alias-and-name-false',
        730     )
    --> 732 return cls.__pydantic_validator__.validate_python(
            cls.__pydantic_validator__ = SchemaValidator(title="Book", validator=Model(
        ModelValidator {
            revalidate: Never,
            validator: ModelFields(
                ModelFieldsValidator {
                    fields: [
                        Field {
                            name: "title",
                            lookup_path_collection: LookupPathCollection {
                                by_name: LookupPath {
                                    first_item: PathItemString(
                                        "title",
                                    ),
                                    rest: [],
                                },
                                by_alias: [],
                            },
                            validator: Str(
                                StrValidator {
                                    strict: false,
                                    coerce_numbers_to_str: false,
                                },
                            ),
                            frozen: false,
                        },
                        Field {
                            name: "pages",
                            lookup_path_collection: LookupPathCollection {
                                by_name: LookupPath {
                                    first_item: PathItemString(
                                        "pages",
                                    ),
                                    rest: [],
                                },
                                by_alias: [],
                            },
                            validator: ConstrainedInt(
                                ConstrainedIntValidator {
                                    strict: false,
                                    multiple_of: None,
                                    le: None,
                                    lt: None,
                                    ge: None,
                                    gt: Some(
                                        I64(
                                            0,
                                        ),
                                    ),
                                },
                            ),
                            frozen: false,
                        },
                        Field {
                            name: "authors",
                            lookup_path_collection: LookupPathCollection {
                                by_name: LookupPath {
                                    first_item: PathItemString(
                                        "authors",
                                    ),
                                    rest: [],
                                },
                                by_alias: [],
                            },
                            validator: List(
                                ListValidator {
                                    strict: false,
                                    item_validator: Some(
                                        Prebuilt(
                                            PrebuiltValidator {
                                                schema_validator: Py(
                                                    0x0000746881cd0dc0,
                                                ),
                                            },
                                        ),
                                    ),
                                    min_length: None,
                                    max_length: None,
                                    name: OnceLock(
                                        <uninit>,
                                    ),
                                    fail_fast: false,
                                },
                            ),
                            frozen: false,
                        },
                    ],
                    model_name: "Book",
                    extra_behavior: Ignore,
                    extras_validator: None,
                    extras_keys_validator: None,
                    strict: false,
                    from_attributes: false,
                    loc_by_alias: true,
                    lookup: LookupTree {
                        inner: {
                            PathItemString(
                                "title",
                            ): LookupTreeNode {
                                fields: [
                                    LookupFieldInfo {
                                        field_index: 0,
                                        lookup_priority: LookupFieldPriority {
                                            lookup_type: Both,
                                            alias_index: 0,
                                        },
                                    },
                                ],
                                map: {},
                                list: {},
                            },
                            PathItemString(
                                "pages",
                            ): LookupTreeNode {
                                fields: [
                                    LookupFieldInfo {
                                        field_index: 1,
                                        lookup_priority: LookupFieldPriority {
                                            lookup_type: Both,
                                            alias_index: 0,
                                        },
                                    },
                                ],
                                map: {},
                                list: {},
                            },
                            PathItemString(
                                "authors",
                            ): LookupTreeNode {
                                fields: [
                                    LookupFieldInfo {
                                        field_index: 2,
                                        lookup_priority: LookupFieldPriority {
                                            lookup_type: Both,
                                            alias_index: 0,
                                        },
                                    },
                                ],
                                map: {},
                                list: {},
                            },
                        },
                    },
                    validate_by_alias: None,
                    validate_by_name: None,
                },
            ),
            class: Py(
                0x000000000e0a8420,
            ),
            generic_origin: None,
            post_init: None,
            frozen: false,
            custom_init: false,
            root_model: false,
            undefined: Py(
                0x00007468d43cdaa0,
            ),
            name: "Book",
        },
    ), definitions=[], cache_strings=True)
            cls = <class '__main__.Book'>
            obj = {'title': 'The Hobbit', 'pages': 300, 'authors': [{'name': 'J.R.R.', 'age': -32, 'email': None}]}
            strict = None
            extra = None
            from_attributes = None
            context = None
            by_alias = None
            by_name = None    733     obj,
        734     strict=strict,
        735     extra=extra,
        736     from_attributes=from_attributes,
        737     context=context,
        738     by_alias=by_alias,
        739     by_name=by_name,
        740 )


    ValidationError: 1 validation error for Book
    authors.0.age
      Input should be greater than 0 [type=greater_than, input_value=-32, input_type=int]
        For further information visit https://errors.pydantic.dev/2.13/v/greater_than


## Restrições numéricas com `Field`

`Field(...)` é a forma declarativa de embutir regras de validação direto na definição do campo — sem escrever validators manualmente.

| Parâmetro | Semântica | Aceita |
|-----------|-----------|--------|
| `gt=N` | estritamente maior que N | `N+1`, `N+2`, … |
| `ge=N` | maior ou igual a N | `N`, `N+1`, … |
| `lt=N` | estritamente menor que N | …, `N-2`, `N-1` |
| `le=N` | menor ou igual a N | …, `N-1`, `N` |


```python
from pydantic_core import ValidationError

# greater_than -> gt
class GreaterThan(BaseModel):
    maiores: int = Field(gt=18)

try:
 GreaterThan(maiores=11)
except ValidationError as exc:
    print("gt ->",repr(exc.errors()[0]['msg']))

try:
    print("18 is not greater than 18")
    GreaterThan(maiores=18)
except ValidationError as exc:
    print("gt ->",repr(exc.errors()[0]['msg']))


```

    gt -> 'Input should be greater than 18'
    18 is not greater than 18
    gt -> 'Input should be greater than 18'



```python
# greater_than_equal -> ge
class GreaterThanEqual(BaseModel):
    maiores: int = Field(ge=18)

try:
    print("17 is not greater than or equal to 18")
    GreaterThanEqual(maiores = 17)
except ValidationError as exc:
    print("ge ->",repr(exc.errors()[0]['msg']))
```

    17 is not greater than or equal to 18
    ge -> 'Input should be greater than or equal to 18'



```python
# less_than -> lt
from pydantic import BaseModel, Field, ValidationError

class Model(BaseModel):
    x: int = Field(lt=10)
try:
    Model(x=10)
except ValidationError as exc:
    print("ls:",repr(exc.errors()[0]['msg']))
    #> 'less_than'


# less_than_equal -> le
class Model(BaseModel):
    x: int = Field(le=10)
try:
    Model(x=11)
except ValidationError as exc:
    print("le:",repr(exc.errors()[0]['msg']))
    #> 'less_than_equal'
```

    ls: 'Input should be less than 10'
    le: 'Input should be less than or equal to 10'


## Restrições em listas com `conlist`

`conlist(T, min_length=N, max_length=M)` é um tipo que declara uma lista de `T` com tamanho controlado.  
Substitui um `field_validator` manual para a restrição mais comum de coleções.


```python
from pydantic import BaseModel, conlist, ValidationError

class Post(BaseModel):
    title: str
    tags: conlist(str, min_length=1, max_length=3)

# OK
p = Post(title="Pydantic", tags=["python", "validation"])
print(p)

# Erro: lista vazia (min_length=1)
try:
    Post(title="Oops", tags=[])
except ValidationError as exc:
    print("lista vazia:",repr(exc.errors()[0]['msg']))

# Erro: lista grande demais (max_length=3)
try:
    Post(title="Oops", tags=["a", "b", "c", "d"])
except ValidationError as exc:
    print("grande demais:",repr(exc.errors()[0]['msg']))
```

    title='Pydantic' tags=['python', 'validation']
    lista vazia: 'List should have at least 1 item after validation, not 0'
    grande demais: 'List should have at most 3 items after validation, not 4'


## Restrições em `Decimal`

Para valores monetários e financeiros, `Decimal` combinado com `Field` oferece controle total sobre dígitos e casas decimais.  
`Annotated[Decimal, Field(...)]` mantém todas as restrições agrupadas na definição do tipo — sem código espalhado.

| Parâmetro | Semântica |
|-----------|-----------|
| `gt` / `ge` / `lt` / `le` | faixa de valores (igual ao `int`/`float`) |
| `multiple_of` | o valor deve ser múltiplo exato do passo |
| `max_digits` | total de dígitos significativos (antes + depois da vírgula) |
| `decimal_places` | máximo de casas decimais |
| `allow_inf_nan` | proíbe `Infinity` e `NaN` |
| `strict` | impede coerção — aceita apenas `Decimal` puro |


```python
from decimal import Decimal
from typing import Annotated
from pydantic import BaseModel, Field, ValidationError

# greater_than -> gt
# greater_than_equal -> ge
# less_than -> lt
# less_than_equal -> le
# multiple_of -> multiple_of
# max_digits -> max_digits
# decimal_places -> decimal_places

class DecimalRules(BaseModel):
    valor: Annotated[
        Decimal,
        Field(
            gt=Decimal("10.00"),
            ge=Decimal("10.50"),
            lt=Decimal("20.00"),
            le=Decimal("19.99"),
            multiple_of=Decimal("0.25"),
            max_digits=6,
            decimal_places=2,
            allow_inf_nan=False,
            strict=True,
        ),
    ]

# OK
ok = DecimalRules(valor=Decimal("10.50"))
print("OK ->", ok)

# Erro ge (e também gt)
try:
    print("10.00 is not greater than or equal to 10.50")
    DecimalRules(valor=Decimal("10.00"))
except ValidationError as exc:
    print("ge ->", repr(exc.errors()[0]["msg"]))

# Erro lt/le
try:
    print("20.00 is not less than 20.00")
    DecimalRules(valor=Decimal("20.00"))
except ValidationError as exc:
    print("lt/le ->", repr(exc.errors()[0]["msg"]))

# Erro multiple_of
try:
    print("10.60 is not a valid multiple of 0.25")
    DecimalRules(valor=Decimal("10.60"))
except ValidationError as exc:
    print("multiple_of ->", repr(exc.errors()[0]["msg"]))

# Erro decimal_places
try:
    print("10.555 has more than 2 decimal places")
    DecimalRules(valor=Decimal("10.555"))
except ValidationError as exc:
    print("decimal_places ->", repr(exc.errors()[0]["msg"]))

# Erro max_digits
try:
    print("12345.67 exceeds max_digits=6")
    DecimalRules(valor=Decimal("12345.67"))
except ValidationError as exc:
    print("max_digits ->", repr(exc.errors()[0]["msg"]))
```

    OK -> valor=Decimal('10.50')
    10.00 is not greater than or equal to 10.50
    ge -> 'Input should be greater than or equal to 10.50'
    20.00 is not less than 20.00
    lt/le -> 'Input should be less than or equal to 19.99'
    10.60 is not a valid multiple of 0.25
    multiple_of -> 'Input should be a multiple of 0.25'
    10.555 has more than 2 decimal places
    decimal_places -> 'Decimal input should have no more than 2 decimal places'
    12345.67 exceeds max_digits=6
    max_digits -> 'Decimal input should have no more than 6 digits in total'


## Validators customizados — `field_validator` e `model_validator`

Quando uma restrição não cabe em `Field`, use decorators de validação para expressar a regra explicitamente.

**Regra de escolha:**

> *"Consigo decidir só com esse campo?"* → `@field_validator`  
> *"Preciso olhar outros campos?"* → `@model_validator`

| Decorator | Parâmetro | Quando usar |
|-----------|-----------|-------------|
| `@field_validator("campo")` | `cls` | regra isolada de um campo |
| `@model_validator(mode="after")` | `self` (instância pronta) | regra entre campos, derivação de valores |


```python
from pydantic import BaseModel, field_validator, model_validator, PositiveInt, ValidationError

class Owner(BaseModel):
    name: str
    title: str | None = None
    name_normalized: str | None = None
    age: PositiveInt

    @field_validator("name")
    @classmethod
    def name_must_contain_space(cls, value: str) -> str:
        if " " not in value:
            raise ValueError("name must contain a space")
        return value

    # "Consigo decidir só com esse campo?” -> field_validator
    # "Preciso olhar outros campos?” -> model_validator
    @field_validator("title", mode="before")
    @classmethod
    def title_to_upper(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.title()

    @model_validator(mode="after")
    def fill_name_normalized(self):
        self.name_normalized = self.name.upper()
        return self


try:
    owner_instance = Owner(name="John", age=20)
except ValidationError as exc:
    print(exc)

owner_instance1 = Owner(name="John Doe", age=20)
print(owner_instance1)

owner_instance2 = Owner(name="John Doe", age=20, title="dr.")
print(owner_instance2)

```

    1 validation error for Owner
    name
      Value error, name must contain a space [type=value_error, input_value='John', input_type=str]
        For further information visit https://errors.pydantic.dev/2.13/v/value_error
    name='John Doe' title=None name_normalized='JOHN DOE' age=20
    name='John Doe' title='Dr.' name_normalized='JOHN DOE' age=20


### Modos de execução: `before` vs `after`

Os validators rodam em momentos diferentes do ciclo de vida da validação.

| Modo | Recebe | Executa | Uso típico |
|------|--------|---------|------------|
| `field_validator(mode="before")` | `cls` + dado bruto | antes da conversão de tipo | normalizar entrada (strip, lowercase) |
| `field_validator(mode="after")` | `cls` + valor já convertido | após conversão do campo | validar regras do campo já tipado |
| `model_validator(mode="before")` | `cls` + dict bruto | antes de criar o modelo | renomear chaves, migrar payloads legados |
| `model_validator(mode="after")` | `self` (instância pronta) | após todos os campos validados | regras cruzadas, derivar campos opcionais |

**`cls` vs `self`**

- `cls` — é a *classe*, não o objeto. Aparece quando a instância ainda não existe.  
- `self` — é a *instância criada*. Disponível apenas em `model_validator(mode="after")`.


```python
from typing import Any
from pydantic import BaseModel, Field, ValidationError, field_validator, model_validator

class UserRegister(BaseModel):
    email: str
    password: str
    confirm_password: str
    age: int = Field(ge=18)
    username: str | None = None

    # FIELD BEFORE:
    # roda antes da validação de tipo/regras do campo
    # útil para limpar/normalizar entrada bruta
    @field_validator("email", mode="before")
    @classmethod
    def clean_email(cls, value: Any) -> Any:
        if isinstance(value, str):
            return value.strip().lower()
        return value

    # FIELD AFTER:
    # roda depois que o campo já foi convertido/validado
    # útil para regra do próprio campo
    # 1.cls
    ## • É a classe (Owner, UserRegister), não o objeto criado.
    ## • Aparece em métodos com @classmethod (como field_validator e model_validator(mode="before")).
    ## • Use quando você está validando/transformando dados antes de existir uma instância ou quando não precisa acessar valores finais via self.
    # 2. self
    ## • É a instância já criada (o objeto com campos validados).
    ## • Aparece em model_validator(mode="after").
    ## • Use quando precisa acessar/relacionar campos já prontos, ex: self.password != self.confirm_password ou preencher self.username.
    @field_validator("password", mode="after")
    @classmethod
    def password_strength(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("password must have at least 8 characters")
        return value

    # MODEL BEFORE:
    # roda antes de criar o modelo
    # útil para ajustar payload inteiro (aliases, chaves antigas, etc.)
    @model_validator(mode="before")
    @classmethod
    def migrate_legacy_keys(cls, data: Any) -> Any:
        if isinstance(data, dict) and "user_email" in data and "email" not in data:
            data["email"] = data.pop("user_email")
        return data

    # MODEL AFTER:
    # roda com o objeto já montado
    # útil para regra entre campos
    @model_validator(mode="after")
    def cross_field_rules(self):
        if self.password != self.confirm_password:
            raise ValueError("password and confirm_password must match")

        if self.username is None:
            self.username = self.email.split("@")[0]

        return self


# OK
u1 = UserRegister(
    user_email="  JOHN.DOE@EXAMPLE.COM ",
    password="abc12345",
    confirm_password="abc12345",
    age=20,
)
print("OK:", u1)

# Erro de model after (campos diferentes)
try:
    UserRegister(
        email="ana@example.com",
        password="abc12345",
        confirm_password="xxxxxx99",
        age=22,
    )
except ValidationError as exc:
    print("\nERRO model after:")
    print(exc)

# Erro de field after (senha curta)
try:
    UserRegister(
        email="ana@example.com",
        password="123",
        confirm_password="123",
        age=22,
    )
except ValidationError as exc:
    print("\nERRO field after:")
    print(exc)
```

    OK: email='john.doe@example.com' password='abc12345' confirm_password='abc12345' age=20 username='john.doe'
    
    ERRO model after:
    1 validation error for UserRegister
      Value error, password and confirm_password must match [type=value_error, input_value={'email': 'ana@example.co...: 'xxxxxx99', 'age': 22}, input_type=dict]
        For further information visit https://errors.pydantic.dev/2.13/v/value_error
    
    ERRO field after:
    1 validation error for UserRegister
    password
      Value error, password must have at least 8 characters [type=value_error, input_value='123', input_type=str]
        For further information visit https://errors.pydantic.dev/2.13/v/value_error


## Valores padrão dinâmicos — `default_factory`

`Field(default_factory=callable)` define um valor calculado **no momento da instanciação**.

- Diferente de `default=valor` (avaliado uma única vez no carregamento do módulo), o callable é invocado a cada novo objeto.
- Essencial para mutáveis (`list`, `dict`) e para identificadores únicos (`uuid4`).


```python
from uuid import uuid4
from pydantic import BaseModel, Field, UUID4

class DefaultFactoryModel(BaseModel):
    x: UUID4 = Field(default_factory=uuid4)
    y: int = Field(default_factory=lambda: uuid4().int)
    # int não preserva zeros à esquerda; por isso, para exibir 5 dígitos visuais, usamos str.
    z: str = Field(default_factory=lambda: f"{uuid4().int % 100000:05d}")

print(DefaultFactoryModel())
```

    x=UUID('f1f8ca65-f1ae-493c-bd14-2bf371e598df') y=269602825914735625145026726063535486866 z=1980


## Aliases de campo — `Field(alias=...)`

`alias` desacopla o **nome externo** (JSON, API, banco) do **nome interno** Python.

- A instância é criada usando o alias (`username="john_doe"`).  
- `model_dump(by_alias=True)` serializa com o nome externo.  
- `model_dump(by_alias=False)` (padrão) usa o nome Python.


```python
class AliasModel(BaseModel):
    name: str = Field(..., alias="username")

user = AliasModel(username="john_doe")
print(user.name)
print(user.model_dump(by_alias=True))  # {'username': 'john_doe'}
print(user.model_dump(by_alias=False))  # {'name': 'john_doe'}
```

    john_doe
    {'username': 'john_doe'}
    {'name': 'john_doe'}


## Campos calculados — `@computed_field`

`@computed_field` expõe uma `@property` como campo do modelo: aparece em `model_dump()` e no `repr`, mas não é armazenado separadamente.

Útil para derivar valores de outros campos (ex.: `age` a partir de `birth_year`) e combiná-los com `model_validator` para regras de negócio.


```python
from datetime import datetime
from pydantic import BaseModel, computed_field, model_validator

class Person(BaseModel):
    name: str
    birth_year: int

    @computed_field
    @property
    def age(self) -> int:
        current_year = datetime.now().year
        return current_year - self.birth_year

    @model_validator(mode="after")
    def check_age(self):
        if self.age < 18:
            raise ValueError("Person must be at least 18 years old")
        return self
try:
    person = Person(name="Alice", birth_year=2015)
except ValidationError as exc:
    print("max_digits ->", repr(exc.errors()[0]["msg"]))
```

    max_digits -> 'Value error, Person must be at least 18 years old'


## Parsing de dados externos

`model_validate(dict)` aceita qualquer dicionário — inclusive o retorno direto de uma API HTTP.  
O Pydantic converte e valida os tipos automaticamente; tipos especiais como `EmailStr` e `HttpUrl` são verificados sem código extra.

O `field_validator(mode="before")` no campo `website` normaliza domínios sem protocolo (`hildegard.org` → `https://hildegard.org`) antes que `HttpUrl` tente parsear.


```python
import httpx
import httpx
from pydantic import BaseModel, EmailStr, HttpUrl, field_validator


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str | None = None
    website: HttpUrl | None = None

    @field_validator("website", mode="before")
    @classmethod
    def normalize_website(cls, value):
        if value is None:
            return None

        if isinstance(value, str):
            value = value.strip()
            if value == "":
                return None
            # Normalize bare domains to valid URLs for HttpUrl parsing
            if "://" not in value:
                value = f"https://{value}"

        return value



url = 'https://jsonplaceholder.typicode.com/users/1'

response = httpx.get(url)
response.raise_for_status()

user = User.model_validate(response.json())
print(repr(user))


```

    User(id=1, name='Leanne Graham', email='Sincere@april.biz', phone='1-770-736-8031 x56442', website=HttpUrl('https://hildegard.org/'))


### Validando listas com `TypeAdapter`

Quando a resposta da API é uma lista (não um único objeto), use `TypeAdapter(list[Model])`.  
`TypeAdapter` aplica a mesma validação do `BaseModel` a qualquer tipo Python, incluindo coleções genéricas — sem precisar criar um modelo wrapper só para envolver a lista.


```python
from pprint import pprint
import httpx
from pydantic import BaseModel, EmailStr, TypeAdapter

class User(BaseModel):
  id: int
  name: str
  email: EmailStr

url = 'https://jsonplaceholder.typicode.com/users/'

response = httpx.get(url)
response.raise_for_status()
users_list_adapter = TypeAdapter(list[User])
users = users_list_adapter.validate_python(response.json())
pprint([u.name for u in users])
"""
['Leanne Graham',
'Ervin Howell',
'Clementine Bauch',
'Patricia Lebsack',
'Chelsey Dietrich',
'Mrs. Dennis Schulist',
'Kurtis Weissnat',
'Nicholas Runolfsdottir V',
'Glenna Reichert',
'Clementina DuBuque']
"""
```

    ['Leanne Graham',
     'Ervin Howell',
     'Clementine Bauch',
     'Patricia Lebsack',
     'Chelsey Dietrich',
     'Mrs. Dennis Schulist',
     'Kurtis Weissnat',
     'Nicholas Runolfsdottir V',
     'Glenna Reichert',
     'Clementina DuBuque']





    "\n['Leanne Graham',\n'Ervin Howell',\n'Clementine Bauch',\n'Patricia Lebsack',\n'Chelsey Dietrich',\n'Mrs. Dennis Schulist',\n'Kurtis Weissnat',\n'Nicholas Runolfsdottir V',\n'Glenna Reichert',\n'Clementina DuBuque']\n"


