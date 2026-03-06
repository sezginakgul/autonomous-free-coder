export default function ProductGrid({products,add}){

return(

<div className="grid grid-cols-3 gap-4 p-4">

{products.map(p=>(

<div
key={p.id}
onClick={()=>add(p)}
className="bg-white rounded-xl shadow-sm hover:shadow-md cursor-pointer p-3">

<img src={p.image} className="rounded-lg"/>

<h3 className="font-semibold mt-2">
{p.name}
</h3>

<p className="text-sm text-gray-500">
{p.price}₺
</p>

</div>

))}

</div>

)

}