// function fun1(fun) {
//     console.log("yup", fun())
// }

// fun1(() => { const x = 100; })

// import c2 from "./rough2"


// c11 = new c1()
// c11.fun1()
// console.log(this)

// window1 = {
//     x: "x in window obj",
//     onClick1: () => null
// }

// // window1.onclick1 = () => { console.log("tinku") }

// class c1 {
//     constructor(x) {
//         this.x = x;
//         this.fun1 = this.fun1.bind(this)
//     }
//     fun1() {
//         console.log("in fun1()");
//         console.log(this.x)
//     }
//     fun2() {
//         window1.onClick1 = this.fun1
//         console.log("this is a method")
//     }
// }
// c11 = new c1("c1")
// c11.fun2()

// function fun3() {
//     console.log("this is a fucntion")
// }

// window1.onClick1()

// const obj1 = {
//     1: "tinku"
// }

// const obj2 = {
//     1: "kalluri"
// }

// console.log({ ...obj1, ...obj2 })




function _sort(arr) {
    arr.sort((a, b) => {
        var t1 = date_timeParser(a)
        var t2 = date_timeParser(b)
        if (t1.date.y < t2.date.y) {
            return -3;
        } else if (t1.date.y > t2.date.y) {
            return 3
        } else if (t1.date.y == t2.date.y) {
            if (t1.date.m < t2.date.m) {
                return -3;
            } else if (t1.date.m > t2.date.m) {
                return 3
            } else if (t1.date.m == t2.date.m) {
                if (t1.date.d < t2.date.d) {
                    return -3;
                } else if (t1.date.d > t2.date.d) {
                    return 3
                } else if (t1.date.d == t2.date.d) {
                    if (t1.time.h < t2.time.h) {
                        return -4;
                    } else if (t1.time.h > t2.time.h) {
                        return 3;
                    } else if (t1.time.h == t2.time.h) {
                        if (t1.time.m < t2.time.m) {
                            return -4;
                        } else if (t1.time.m > t2.time.m) {
                            return 3;
                        } else if (t1.time.m == t2.time.m) {
                            if (t1.time.s < t2.time.s) {
                                return -4;
                            } else if (t1.time.s > t2.time.s) {
                                return 3;
                            } else if (t1.time.s == t2.time.s) {
                                if (t1.time.ns < t2.time.ns) {
                                    return -4;
                                } else if (t1.time.ns > t2.time.ns) {
                                    return 3;
                                } else if (t1.time.ns == t2.time.ns) {
                                    return 0
                                }
                            }
                        }
                    }
                }
            }
        }
    })
}

function date_timeParser(str) {
    let l1 = str.split('T')
    let date = l1[0].split('-')
    let date_year = date[0].trim()
    let date_month = date[1].trim()
    let date_date = date[2].trim()

    let t = l1[1].split('.')
    let t_ns = t[1]
    t = t[0].split(':')
    let t_h = t[0]
    let t_m = t[1]
    let t_s = t[2]
    return {
        date: {
            d: parseInt(date_date),
            m: parseInt(date_month),
            y: parseInt(date_year)
        },
        time: {
            h: parseInt(t_h),
            m: parseInt(t_m),
            s: parseInt(t_s),
            ns: parseInt(t_ns.replace('Z', ''))
        }
    }
}


str1 = '2022-09-15T02:51:55.952383Z'
str2 = '2022-09-14T01:51:54.952381Z'

console.log(date_timeParser(str1))

arr = [str1, str2]

_sort(arr)

console.log(arr)


