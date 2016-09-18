begin;

create table YPKUser (
  id serial primary key,
  username varchar(512) not null unique,
  password varchar(512) not null,
  registered_at timestamptz not null default CURRENT_DATE,
  is_admin boolean not null default false
);

create table Topping (
  id serial primary key,
  name varchar(512) not null,
  price money not null
);

create table Pizza (
  id serial primary key,
  name varchar(512) not null,
  price money not null
);

create table Pizza_Topping (
  pizza_id int references Pizza (id),
  topping_id int references Topping (id),
  constraint Pizza_Topping_pkey primary key (pizza_id, topping_id)
);

create table Kebab (
  id serial primary key,
  name varchar(512) not null,
  price money not null
);

create table Drink (
  id serial primary key,
  name varchar(512) not null,
  price money not null
);

create table Discount (
  id serial primary key,
  name varchar(512) not null,
  percentage_off int not null
);

create table YPKOrder (
  id serial primary key,
  ordered_by integer references YPKUser (id) not null,
  ordered_at timestamptz not null default CURRENT_DATE,
  modified_at timestamptz,
  discount_id integer references Discount (id),
  paid boolean default false,
  paid_at timestamptz,
  delivery_address varchar(512) not null,
  delivery_at timestamptz not null,
  canceled boolean not null default false,
  rejected boolean not null default false
);

create table DeliverySummary (
  id serial primary key,
  customer_found boolean not null,
  delivered_at timestamptz,
  had_problems boolean not null,
  order_id integer references YPKOrder (id)
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

create table YPKOrder_Drink (
  order_id int references YPKOrder (id),
  drink_id int references Drink (id),
  constraint YPKOrder_Drink_pkey primary key (order_id, drink_id)
);

create table YPKOrder_Pizza_Extra_Topping (
  order_id int references YPKOrder (id),
  pizza_id int references Pizza (id),
  topping_id int references Topping (id),
  constraint YPKOrder_Pizza_Extra_Topping_pkey primary key (order_id, pizza_id, topping_id)
);

commit;
