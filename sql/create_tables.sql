begin;

create table YPKUser (
id serial primary key,
username varchar(50) not null,
password varchar(50) not null,
registered_at date not null default CURRENT_DATE,
is_admin boolean not null default false
);

create table Topping (
id serial primary key,
name varchar(50) not null,
price money not null
);

create table Pizza (
id serial primary key,
name varchar(50) not null,
price money not null
);

create table Pizza_Topping (
pizza_id int references Pizza (id),
topping_id int references Topping (id),
constraint Pizza_Topping_pkey primary key (pizza_id, topping_id)
);

create table Kebab (
id serial primary key,
name varchar(50) not null,
price money not null
);

create table Discount (
id serial primary key,
name varchar(50) not null,
percentage_off int not null
);

create table YPKOrder (
id SERIAL primary key,
ordered_by integer references YPKUser(id) not null,
ordered_at date not null default CURRENT_DATE,
modified_at date,
discount integer references Discount(id),
paid boolean default false,
paid_at date
);

create table YPKOrder_Pizza (
order_id int references YPKOrder (id),
pizza_id int references Pizza (id),
oregano_enabled boolean not null default false,
garlic_enabled boolean not null default false,
constraint YPKOrder_Pizza_pkey primary key (order_id, pizza_id)
);

create table YPKOrder_Kebab (
order_id int references YPKOrder (id),
kebab_id int references Kebab (id),
constraint YPKOrder_Kebab_pkey primary key (order_id, kebab_id)
);

create table YPKOrder_Pizza_Extra_Topping (
order_id int references YPKOrder (id),
pizza_id int references Pizza (id),
topping_id int references Topping (id),
constraint YPKOrder_Pizza_Extra_Topping_pkey primary key(order_id, pizza_id, topping_id)
);

commit;
