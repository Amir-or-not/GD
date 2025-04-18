drop table liked cascade;
drop table archive cascade;
drop table cart cascade;                                                                                                    --udalenie tablic
drop table products cascade;
drop table users cascade;

-----------------------------------------------------------------------------------------------

create table users ( 
user_id serial primary key, 
username text not null, 
password_hash varchar(255) not null, 
email varchar(255) not null unique, 
role text not null check (role in ('admin', 'user', 'seller')),
created_at timestamp default current_timestamp,
avatar varchar(255),
salt bytea not null
);

create table products (
product_id serial primary key,
product_name varchar(255) not null,
description text,
product_category text,
image varchar(255),
posted_at timestamp default current_timestamp,                                                                                   --tablicy
price float not null,
amount int not null check (amount >= 0)
);

create table cart (
user_id int,
product_id int,
quantity int not null default 1 check (quantity > 0),
added_at timestamp default current_timestamp,
primary key (user_id, product_id),
foreign key (user_id) references users(user_id) on delete cascade,
foreign key (product_id) references products(product_id) on delete cascade
);

create table archive (
archive_id serial primary key,
user_id int,
product_id int,
quantity int not null default 1,
purchase_date timestamp default current_timestamp,
foreign key (user_id) references users(user_id) on delete set null,
foreign key (product_id) references products(product_id) on delete set null
);

create table liked (
user_id int,
product_id int,
primary key (user_id, product_id),
foreign key (user_id) references users(user_id) on delete cascade,
foreign key (product_id) references products(product_id) on delete cascade
);

-----------------------------------------------------------------------------------------------

insert into users(username,password_hash,email,role,created_at,avatar,salt)
values
('niko','hohoho','niko@gmail.com','user','09.04.25','niko.jpg','1234'),
('amr','amr123','amik@gmail.com','admin','01.04.25','amirro.jpg','12345'),
('mans','raiden321','mukyn@gmail.com','seller','05.04.25','mukinov.jpg','322');                               --vvod informacii (oni po suti nujny dl9 primera)

insert into products(product_name, description, product_category, image, price, amount)
values
('knife','very sharp','self defend','knife.jpg',999.90,10),
('ring','very pretty','accessory','ring.png',23999.90,5);

-----------------------------------------------------------------------------------------------

update users
set role = 'user' --vyberite role, tipo user,admin,seller                                                                 --obnovlenie rolei
where email = 'niko@gmail.com'; --vvedite email (email potomu 4to on doljen byt' unikal'nym i tak leg4e)

-----------------------------------------------------------------------------------------------

select * from users
order by user_id;
																														--vyvod informacii
select * from products
order by price;

-----------------------------------------------------------------------------------------------

create table ai(
id serial primary key,
response text,
answer text
);


insert into products(product_name, description, product_category, image, price, amount)
values
('ganyu','perfect','for myself','https://i.pinimg.com/736x/a2/72/29/a27229e09f070076456dff9dffa31200.jpg',999.90,10);


insert into products(product_name, description, product_category, image, price, amount)
values
('ganyu','perfect','for myself', '/static/images/g.webp', 1000000, 20);



insert into cart(user_id, product_id, quantity)
values
(1,1,10);