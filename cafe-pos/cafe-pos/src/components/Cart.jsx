export default function Cart({cart,inc,dec}){

const total = cart.reduce((t,i)=>t+i.price*i.qty,0)

return(

<div className="bg-white shadow-md p-4 flex flex-col h-full">

<h2 className="font-bold mb-4">Adisyon</h2>

<div className="flex-1 space-y-3">

{cart.map(item=>(

<div key={item.id} className="flex justify-between items-center">

<div>

<p>{item.name}</p>

<p className="text-sm text-gray-500">{item.price}₺</p>

</div>

<div className="flex items-center gap-2">

<button onClick={()=>dec(item.id)}>-</button>

<span>{item.qty}</span>

<button onClick={()=>inc(item.id)}>+</button>

</div>

</div>

))}

</div>

<div className="border-t pt-3">

<p className="font-bold">Toplam: {total}₺</p>

<button className="mt-3 w-full bg-green-600 text-white p-3 rounded-xl">

Ödeme Yap

</button>

</div>

</div>

)

}